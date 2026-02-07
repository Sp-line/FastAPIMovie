from pydantic import BaseModel, ConfigDict


class Id(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Pagination(BaseModel):
    skip: int = 0
    limit: int = 100
