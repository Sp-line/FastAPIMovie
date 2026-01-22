from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper as db
from repositories.unit_of_work import UnitOfWork


def get_uow(session: Annotated[AsyncSession, Depends(db.session_getter)]) -> UnitOfWork:
    return UnitOfWork(session)