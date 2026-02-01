from pydantic import BaseModel, ConfigDict


class Id(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)