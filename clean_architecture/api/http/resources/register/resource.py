from fastapi import Depends

from clean_architecture.api.http.common import Resource
from clean_architecture.applications import MediatorGetter, AccountRegisterCommand
from clean_architecture.infrastructure import InMemoryInjector
from .request import RegisterRequest


class RegisterResource(Resource):
    def __init__(self):
        super(RegisterResource, self).__init__()
        self.router.add_api_route('/register', self.register, methods=['POST'], status_code=200)

    @staticmethod
    async def register(request: RegisterRequest = Depends(RegisterRequest)):
        mediator = MediatorGetter.get_mediator('command', injector=InMemoryInjector())
        payload = await request.get_payload()
        payload = payload.dict()
        await mediator.handle(AccountRegisterCommand(payload['name'],
                                                     payload['email'],
                                                     payload['password'],
                                                     payload['executed_at']))
        return {'message': 'Account created'}
