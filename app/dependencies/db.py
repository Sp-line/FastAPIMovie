from typing import Annotated, TypeAlias

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper as db
from repositories.unit_of_work import UnitOfWork

AsyncSessionDep: TypeAlias = Annotated[AsyncSession, Depends(db.session_getter)]


def get_uow(session: AsyncSessionDep) -> UnitOfWork:
    return UnitOfWork(session)


UnitOfWorkDep: TypeAlias = Annotated[UnitOfWork, Depends(get_uow)]
