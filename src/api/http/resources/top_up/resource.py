from fastapi import Depends

from src.api.http.common import Resource
from src.applications import MediatorGetter, BalanceTopUpCommand
from src.infrastructure import in_memory_injector
from .request import TopUpRequest


class TopUpResource(Resource):
    def __init__(self):
        super(TopUpResource, self).__init__()
        self.router.add_api_route('/top-up', self.top_up, methods=['POST'], status_code=200)

    @staticmethod
    async def top_up(request: TopUpRequest = Depends(TopUpRequest)):
        mediator = MediatorGetter.get_mediator('command', injector=in_memory_injector.clone())
        email = request.get_auth().email
        payload = await request.get_payload()
        await mediator.handle(BalanceTopUpCommand(email, **payload.dict()))
        return {'message': 'Top up successfully '}
