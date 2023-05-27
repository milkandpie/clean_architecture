from fastapi import Depends

from src.api.http.common import Resource
from src.applications import MediatorGetter, AccountLoginCommand
from src.infrastructure import in_memory_injector
from .request import LoginRequest


class LoginResource(Resource):
    def __init__(self):
        super(LoginResource, self).__init__()
        self.router.add_api_route('/login', self.top_up, methods=['POST'], status_code=200)

    @staticmethod
    async def top_up(request: LoginRequest = Depends(LoginRequest)):
        mediator = MediatorGetter.get_mediator('command', injector=in_memory_injector)
        payload = await request.get_payload()
        await mediator.handle(AccountLoginCommand(payload.email, payload.password))
        return {'message': 'Login successfully'}
