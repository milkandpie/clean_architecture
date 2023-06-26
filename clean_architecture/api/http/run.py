import uvicorn
from fastapi import FastAPI

from clean_architecture.api.http.common import APIFactory, APICreatable
from clean_architecture.api.http.config import API_DEBUG
from clean_architecture.api.http.resources import (
    TopUpResource,
    RegisterResource,
    LoginResource)


class AuthAPIFactory(APICreatable):
    def __init__(self):
        self.__factory = APIFactory([TopUpResource(), RegisterResource(), LoginResource()],
                                    name='API',
                                    on_start_up=[],
                                    debug=API_DEBUG)

    def create_app(self) -> FastAPI:
        return self.__factory.create_app()


if __name__ == '__main__':
    app = AuthAPIFactory().create_app()
    uvicorn.run(app)
