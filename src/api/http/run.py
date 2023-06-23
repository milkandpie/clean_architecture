import uvicorn
from fastapi import FastAPI

from src.api.http.config import API_DEBUG
from src.api.http.common import APIFactory, APICreatable
from src.infrastructure import init_collections


class AuthAPIFactory(APICreatable):
    def __init__(self):
        self.__factory = APIFactory([],
                                    name='',
                                    on_start_up=[init_collections],
                                    debug=API_DEBUG)

    def create_app(self) -> FastAPI:
        return self.__factory.create_app()


if __name__ == '__main__':
    app = AuthAPIFactory().create_app()
    uvicorn.run(app)
