from typing import Self

from signals.event_session import EventSession


class UnitOfWork:
    def __init__(self, session: EventSession) -> None:
        self._session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
            self,
            exc_type: object | None,
            exc_val: BaseException | None,
            exc_tb: object | None,
    ) -> None:
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
