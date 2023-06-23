from fastapi import Depends

from src.api.http.resources.resource import Resource
from src.applications import MediatorGetter, BalanceTopUpCommand
from .request import TopUpRequest


class BaseResource(Resource):
    def __init__(self):
        super(BaseResource, self).__init__()
        self.router.add_api_route('top-up', self.post, methods=['POST'], status_code=200)

    async def post(self, request: TopUpRequest = Depends(TopUpRequest)):
        mediator = MediatorGetter.get_mediator('command')
        email = request.get_auth().email
        payload = await request.get_payload()
        await mediator.handle(BalanceTopUpCommand(email, **payload.dict()))
        return {}
