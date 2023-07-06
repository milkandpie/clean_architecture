import json
import re
from abc import (
    ABC,
    abstractmethod)
from typing import (
    Tuple,
    List)

from fastapi import (
    Request,
    Depends,
    Query)
from pydantic import BaseModel


class RequestGettable(ABC):
    @abstractmethod
    def get_request(self) -> Request:
        pass


class BasedRequest(RequestGettable):
    def __init__(self, request: Request):
        self.__request = request

    def get_request(self) -> Request:
        return self.__request


class PayloadRequested(ABC):
    @abstractmethod
    async def get_payload(self) -> BaseModel | List[BaseModel]:
        pass


class PayloadRequest(PayloadRequested):
    def __init__(self, payload: BaseModel | List[BaseModel]):
        self.__payload = payload

    async def get_payload(self) -> BaseModel | List[BaseModel]:
        return self.__payload


class IdRequested(ABC):
    @abstractmethod
    def get_id(self) -> str | None:
        pass


class URLParamsRequested(ABC):
    @abstractmethod
    def get_query(self) -> str | None:
        pass

    @abstractmethod
    def get_sort(self) -> Tuple[str, int] | None:
        pass

    @abstractmethod
    def get_limit(self) -> int:
        pass

    @abstractmethod
    def get_offset(self) -> int:
        pass

    @abstractmethod
    def get_filters(self) -> dict:
        pass


class IdRequest(IdRequested, RequestGettable):
    def __init__(self, based_request: RequestGettable = Depends(BasedRequest),
                 model_id: str = Query(alias='id',
                                       description="Query param's document id",
                                       example='63b1d5334689f2b64923d845',
                                       default=None,
                                       min_length=12,
                                       max_length=24)):
        self.__based_request = based_request
        self.__model_id = model_id

    def get_id(self) -> str | None:
        request = self.get_request()
        model_id = request.path_params.get('model_id') or self.__model_id
        if model_id and len(model_id) not in {12, 24}:
            raise ValueError('Invalid model id.')

        return model_id

    def get_request(self) -> Request:
        return self.__based_request.get_request()


class URLParamsRequest(URLParamsRequested, IdRequested, RequestGettable):
    __sort_regex = r'([-+]?)([_\w]+)'

    def __init__(self,
                 id_gettable: IdRequest = Depends(IdRequest),
                 based_request: BasedRequest = Depends(BasedRequest),
                 limit: int = Query(description="Number of returned results. For pagination.",
                                    default=20,
                                    ge=0),
                 offset: int = Query(description="Bypass numbers of result. For pagination.",
                                     default=0,
                                     ge=0),
                 filters: str = Query(description="For db query. Implementation of mongodb filters",
                                      example="{'created': {'$ge': '2022-12-23T07:49:03.383000'}}",
                                      default="{}"),
                 sort: str = Query(regex=__sort_regex,
                                   description="For sorting results with field by order. Default is ascending",
                                   default='', example="Ascending sorting with created  +created, "
                                                       "descending sorting with created: -created"),
                 q: str = Query(default=None,
                                description="For filtering results. Input value used in text query")):

        self.__q = q
        self.__sort = sort
        self.__limit = limit
        self.__offset = offset
        self.__filters = filters
        self.__id_gettable = id_gettable
        self.__based_request = based_request

    def get_request(self) -> Request:
        return self.__based_request.get_request()

    def get_query(self) -> str | None:
        return self.__q

    def get_id(self) -> str | None:
        return self.__id_gettable.get_id()

    def get_sort(self) -> Tuple[str, int] | None:
        sort = self.__sort
        if not sort:
            return

        mapping = {
            '+': 1,
            '-': -1
        }

        match = re.search(self.__sort_regex, sort)
        sort_str = match.group(2)
        order_indicator = match.group(1)

        return sort_str, mapping.get(order_indicator, 1)

    def get_limit(self) -> int:
        limit = self.__limit

        try:
            return int(limit)
        except TypeError:
            raise ValueError(f'Invalid limit params')

    def get_offset(self) -> int:
        try:
            return int(self.__offset)
        except TypeError:
            raise ValueError(f'Invalid offset params')

    def get_filters(self) -> dict:
        try:
            filters = self.__filters or '{}'
            return json.loads(filters.replace("'", "\""))
        except json.JSONDecodeError:
            raise ValueError(f'Invalid filters params')


class BasedPayloadRequest(PayloadRequested, RequestGettable):
    def __init__(self, payload: BaseModel | List[BaseModel],
                 params_requested: RequestGettable = Depends(BasedRequest)):
        self.__params_requested = params_requested
        self.__payload_requested = PayloadRequest(payload)

    async def get_payload(self) -> BaseModel | List[BaseModel]:
        return await self.__payload_requested.get_payload()

    def get_request(self) -> Request:
        return self.__params_requested.get_request()


class IdPayloadRequest(PayloadRequested, IdRequested, RequestGettable):
    def __init__(self, payload: BaseModel | List[BaseModel],
                 params_requested: IdRequest = Depends(IdRequest)):
        self.__params_requested = params_requested
        self.__payload_requested = PayloadRequest(payload)

    async def get_payload(self) -> BaseModel | List[BaseModel]:
        return await self.__payload_requested.get_payload()

    def get_id(self) -> str | None:
        return self.__params_requested.get_id()

    def get_request(self) -> Request:
        return self.__params_requested.get_request()
