from abc import ABC

from pydantic import BaseModel

from repositories.base import IntRepositoryBase, M2MRepositoryBase
from schemas.m2m import CompositeIdBase
from services.abc import ServiceABC


class IntServiceABC[
    IntRepositoryBaseType: IntRepositoryBase,
    ReadSchemaType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    DBCreateSchemaType: BaseModel,
    DBUpdateSchemaType: BaseModel,
](
    ServiceABC[
        int,
        IntRepositoryBaseType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
        DBCreateSchemaType,
        DBUpdateSchemaType
    ],
    ABC
):
    pass


class M2MServiceABC[
    M2MRepositoryBaseType: M2MRepositoryBase,
    ReadSchemaType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    CompositeIdSchemaType: CompositeIdBase,
    DBCreateSchemaType: BaseModel,
    DBUpdateSchemaType: BaseModel,
](
    ServiceABC[
        CompositeIdSchemaType,
        M2MRepositoryBaseType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
        DBCreateSchemaType,
        DBUpdateSchemaType
    ],
    ABC
):
    pass
