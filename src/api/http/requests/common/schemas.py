from pydantic import BaseModel


class DeleteSchema(BaseModel):
    id: str
