from fastapi import APIRouter


from abc import (ABC, abstractmethod)
from typing import List, Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from clean_architecture.api.http.config import CORS_ORIGINS
from clean_architecture.domains import (
    DomainException,
    IncorrectDomainValuedException)


async def method_not_allow_handler(_, __):
    return JSONResponse({'message': 'Method not allowed'}, status_code=405)


async def value_error_handler(_, __):
    return JSONResponse({'message': 'Bad request'}, status_code=400)


async def unique_error_handler(_, exception):
    return JSONResponse({'message': str(exception)}, status_code=403)


async def not_found_error_handler(_, __):
    return JSONResponse({'message': 'Not found'}, status_code=404)


async def unauthorized_error_handler(_, exception):
    message = str(exception) or 'Unauthorized'
    return JSONResponse({'message': message}, status_code=401)


async def unavailable_error_handler(_, exception):
    message = str(exception) or 'Unavailable'
    return JSONResponse({'message': message}, status_code=503)


async def domain_error_handler(_, exception: DomainException):
    return JSONResponse({'message': str(exception)}, status_code=500)


async def domain_value_error_handler(_, exception: IncorrectDomainValuedException):
    return JSONResponse({'message': str(exception)}, status_code=422)


class Resource:
    def __init__(self):
        self.router = APIRouter()


class APICreatable(ABC):
    @abstractmethod
    def create_app(self) -> FastAPI:
        pass


class APIFactory(APICreatable):
    def __init__(self, routes: List[Resource],
                 name: str = None,
                 debug: bool = None,
                 prefix: str = None,
                 description: str = None,
                 on_start_up: List[Callable] = None):
        self.__name = name
        self.__routes = routes
        self.__prefix = prefix
        self.__debug = debug or False
        self.__on_start_up = on_start_up
        self.__description = description

    def create_app(self) -> FastAPI:
        app = FastAPI(title=self.__name,
                      debug=self.__debug,
                      description=self.__description,
                      root_path=self.__prefix)

        for resource in self.__routes:
            app.include_router(resource.router)

        app.add_exception_handler(DomainException, domain_error_handler)
        app.add_exception_handler(IncorrectDomainValuedException, domain_value_error_handler)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.on_event('startup')
        async def collections_initialized():
            for _callable in self.__on_start_up:
                await _callable()

        if not self.__debug:
            app.add_exception_handler(ValueError, value_error_handler)

        return app
