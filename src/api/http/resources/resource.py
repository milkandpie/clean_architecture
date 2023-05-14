from fastapi import APIRouter


class Resource:
    def __init__(self):
        self.router = APIRouter()
