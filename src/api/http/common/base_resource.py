from typing import List

import inflect
from fastapi import (
    Depends,
    HTTPException)
from pymongo.client_session import ClientSession

from src.api.http.common.requests import (
    BasedPayloadRequest,
    IdPayloadRequest,
    URLParamsRequest)
from common import MongoClientFactory
from config import GENERAL_MONGO_CONFIG
from services import (
    DocumentCreatableService,
    DocumentUpdatableService,
    DocumentDeletableService,
    AsyncModelCreatable,
    AsyncModelUpdatable,
    AsyncModelDeletable)
from src.api.http.common.resource import Resource
from exceptions import ServiceException

from src.applications import ListableParams, GettableParams, CountableParams, QueryRepository

p = inflect.engine()


class BaseResource(Resource):
    def __init__(self,
                 path: str = None,
                 mongo_config: dict = None):
        super(BaseResource, self).__init__()
        path = path or f'/{p.plural(self.create_document().__name__.lower())}'
        self.__mongo_config = mongo_config or GENERAL_MONGO_CONFIG

        self.router.add_api_route(path, self.get, methods=['GET'], status_code=200)
        self.router.add_api_route(path, self.post, methods=['POST'], status_code=201)
        self.router.add_api_route(path, self.patch, methods=['PATCH'], status_code=200)
        self.router.add_api_route(path, self.delete, methods=['DELETE'], status_code=204)

        model_id = '{model_id}'
        self.router.add_api_route(f'{path}/{model_id}', self.get, methods=['GET'], status_code=200)
        self.router.add_api_route(f'{path}/{model_id}', self.patch, methods=['PATCH'], status_code=200)
        self.router.add_api_route(f'{path}/{model_id}', self.delete, methods=['DELETE'], status_code=204)

    def _create_queryable(self, **kwargs) -> QueryRepository:
        pass

    def _create_creatable(self, session: ClientSession | None = None,
                          request: BasedPayloadRequest = None,
                          **kwargs) -> AsyncModelCreatable:
        return DocumentCreatableService(self.create_document(), session=session)

    def _create_updatable(self, session: ClientSession | None = None,
                          request: IdPayloadRequest = None,
                          **kwargs) -> AsyncModelUpdatable:
        return DocumentUpdatableService(self.create_document(), session=session)

    def _create_deletable(self, session: ClientSession | None = None,
                          request: IdPayloadRequest = None,
                          **kwargs) -> AsyncModelDeletable:
        return DocumentDeletableService(self.create_document(), session=session)

    async def get(self, request: URLParamsRequest = Depends(URLParamsRequest)):
        repository = self._create_queryable(request=request)
        model_id = request.get_id()

        if model_id:
            model = await repository.get(GettableParams(model_id))
            if not model:
                raise HTTPException(404, {'message': 'Not found'})

            return model.dict()

        total = await repository.count(CountableParams(request.get_query(),
                                                       request.get_filters()))

        sort, order = request.get_sort()
        models = await repository.list(ListableParams(request.get_query(),
                                                      sort,
                                                      order,
                                                      request.get_limit(),
                                                      request.get_offset(),
                                                      request.get_filters()))

        return {'items': models,
                'meta': {'total': total,
                         'limit': request.get_limit(),
                         'offset': request.get_offset()}}

    async def post(self, request: BasedPayloadRequest = Depends(BasedPayloadRequest)):
        factory = MongoClientFactory()
        client = factory.create(self.__mongo_config)
        async with await client.start_session() as session:
            async with session.start_transaction():
                service = self._create_creatable(session=session, request=request)
                multitude = await request.get_payload()
                if not isinstance(multitude, List):
                    multitude = [multitude] if multitude else []

                models = []
                for item in multitude:
                    model = await service.create(attributes=item.dict())
                    models.append(model.dict())

                return {'items': models,
                        'meta': {'total': len(models)}}

    async def patch(self, request: IdPayloadRequest = Depends(IdPayloadRequest)):
        payload = await request.get_payload()
        if not payload:
            return ServiceException('Required payload', code=400)

        factory = MongoClientFactory()
        client = factory.create(self.__mongo_config)

        async with await client.start_session() as session:
            async with session.start_transaction():
                service = self._create_updatable(session=session, request=request)
                model_id = request.get_id()

                if model_id:
                    if isinstance(payload, List):
                        payload = payload[0]

                    await service.update(model_id, attributes=payload.dict())
                    return {'_id': model_id}

                # Without pathed id or params id, search for id in request's payload
                if not isinstance(payload, List):
                    payload = [payload]

                models = []
                for item in payload:
                    attributes = item.dict()
                    item_id = self.__get_item_id(attributes)
                    await service.update(item_id, attributes=attributes)
                    models.append({'_id': item_id})

                return {'items': models,
                        'meta': {'total': len(models)}}

    async def delete(self, request: IdPayloadRequest = Depends(IdPayloadRequest)):
        factory = MongoClientFactory()
        client = factory.create(self.__mongo_config)
        async with await client.start_session() as session:
            async with session.start_transaction():
                service = self._create_deletable(session=session, request=request)
                model_id = request.get_id()

                if model_id:
                    multitude = [model_id]

                else:
                    payload = await request.get_payload()
                    if not isinstance(payload, List):
                        payload = [payload]

                    # Without pathed id or params id, search for id in request's payload
                    multitude = [self.__get_item_id(item.dict()) for item in payload]

                for item_id in multitude:
                    await service.delete(item_id)

                return None

    @staticmethod
    def __get_item_id(item: dict) -> str:
        item_id = item.pop('id', None)
        if not item_id:
            raise ServiceException('Payload required with id field', code=400)

        return item_id
