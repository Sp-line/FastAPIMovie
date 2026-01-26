from pydantic import BaseModel

from repositories.base import IntRepositoryBase, M2MRepositoryBase
from schemas.m2m import CompositeIdBase
from services.abc import ServiceABC


class IntServiceBase[
    IntRepositoryBaseType: IntRepositoryBase,
    ReadSchemaType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
](
    ServiceABC[int, IntRepositoryBaseType, ReadSchemaType, CreateSchemaType, UpdateSchemaType]
):
    pass


class M2MServiceBase[
    M2MRepositoryBaseType: M2MRepositoryBase,
    ReadSchemaType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    CompositeIdSchemaType: CompositeIdBase
](
    ServiceABC[CompositeIdSchemaType, M2MRepositoryBaseType, ReadSchemaType, CreateSchemaType, UpdateSchemaType],
):
    pass
