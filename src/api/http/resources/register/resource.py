from fastapi import Depends

from src.api.http.common import Resource
from src.applications import MediatorGetter, AccountRegisterCommand
from src.infrastructure import in_memory_injector
from .request import RegisterRequest


class RegisterResource(Resource):
    def __init__(self):
        super(RegisterResource, self).__init__()
        self.router.add_api_route('/register', self.top_up, methods=['POST'], status_code=200)

    @staticmethod
    async def top_up(request: RegisterRequest = Depends(RegisterRequest)):
        mediator = MediatorGetter.get_mediator('command', injector=in_memory_injector)
        payload = await request.get_payload()
        payload = payload.dict()
        await mediator.handle(AccountRegisterCommand(payload['name'],
                                                     payload['email'],
                                                     payload['password'],
                                                     payload['executed_at']))
        return {'message': 'Account created'}
