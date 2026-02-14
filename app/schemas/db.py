from pydantic import BaseModel, Field, ConfigDict

from constants.db import PostgresErrorCode
from exceptions.db import DBException


class IntegrityErrorData(BaseModel):
    sqlstate: str
    constraint_name: str
    table_name: str


class ConstraintRule(BaseModel):
    name: str
    error_code: PostgresErrorCode
    exception: DBException

    model_config = ConfigDict(arbitrary_types_allowed=True)
