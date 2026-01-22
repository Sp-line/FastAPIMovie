from typing import TypeVar

from pydantic import BaseModel

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
CompositeIdSchemaType = TypeVar("CompositeIdSchemaType", bound=BaseModel)
