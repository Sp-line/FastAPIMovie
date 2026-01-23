from pydantic import BaseModel


class IntegrityErrorData(BaseModel):
    sqlstate: str
    constraint_name: str
    table_name: str
