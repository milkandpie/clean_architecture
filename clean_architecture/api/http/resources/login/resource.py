from datetime import datetime

from fastapi import Depends, Response

from clean_architecture.api.http.common import Resource
from clean_architecture.applications import MediatorGetter, AccountLoginCommand
from clean_architecture.infrastructure import InMemoryInjector
from .request import LoginRequest


class LoginResource(Resource):
    def __init__(self):
        super(LoginResource, self).__init__()
        self.router.add_api_route('/login', self.login, methods=['POST'], status_code=200)

    @staticmethod
    async def login(response: Response, request: LoginRequest = Depends(LoginRequest)):
        mediator = MediatorGetter.get_mediator('command', injector=InMemoryInjector())
        payload = await request.get_payload()
        payload = payload.dict()
        responses = await mediator.handle(AccountLoginCommand(payload['email'], payload['password'], datetime.utcnow()))
        response.headers['X-Token'] = responses[0]
        return {'message': 'Login successfully'}
