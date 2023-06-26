from fastapi import Depends

from clean_architecture.api.http.common import Resource
from clean_architecture.applications import MediatorGetter, BalanceTopUpCommand
from clean_architecture.infrastructure import InMemoryInjector
from .request import TopUpRequest


class TopUpResource(Resource):
    def __init__(self):
        super(TopUpResource, self).__init__()
        self.router.add_api_route('/top-up', self.top_up, methods=['POST'], status_code=200)

    @staticmethod
    async def top_up(request: TopUpRequest = Depends(TopUpRequest)):
        mediator = MediatorGetter.get_mediator('command', injector=InMemoryInjector())
        email = request.get_auth().email
        payload = await request.get_payload()
        await mediator.handle(BalanceTopUpCommand(email, **payload.dict()))
        return {'message': 'Top up successfully '}
