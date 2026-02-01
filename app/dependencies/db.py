from typing import Annotated, TypeAlias

from fastapi import Depends

from core.models import db_helper as db
from repositories.unit_of_work import UnitOfWork
from signals.event_session import EventSession

EventSessionDep: TypeAlias = Annotated[EventSession, Depends(db.session_getter)]


def get_uow(session: EventSessionDep) -> UnitOfWork:
    return UnitOfWork(session)


UnitOfWorkDep: TypeAlias = Annotated[UnitOfWork, Depends(get_uow)]
