from fastapi import FastAPI

from src.api.http.config import API_DEBUG
from src.api.http.resources import TopUpResource, LoginResource, RegisterResource
from .api_factory import (
    APIFactory,
    APICreatable)


class AuthAPIFactory(APICreatable):
    def __init__(self):
        self.__factory = APIFactory([TopUpResource(),
                                     LoginResource(),
                                     RegisterResource()],
                                    name='Auth resource',
                                    debug=API_DEBUG)

    def create_app(self) -> FastAPI:
        app = self.__factory.create_app()
        return app
