from datetime import datetime

from fastapi import Depends, Response

from src.api.http.common import Resource
from src.applications import MediatorGetter, AccountLoginCommand
from src.infrastructure import in_memory_injector
from .request import LoginRequest


class LoginResource(Resource):
    def __init__(self):
        super(LoginResource, self).__init__()
        self.router.add_api_route('/login', self.top_up, methods=['POST'], status_code=200)

    @staticmethod
    async def top_up(response: Response, request: LoginRequest = Depends(LoginRequest)):
        mediator = MediatorGetter.get_mediator('command', injector=in_memory_injector)
        payload = await request.get_payload()
        payload = payload.dict()
        responses = await mediator.handle(AccountLoginCommand(payload['email'], payload['password'], datetime.utcnow()))
        response.headers['X-Token'] = responses[0]
        return {'message': 'Login successfully'}
