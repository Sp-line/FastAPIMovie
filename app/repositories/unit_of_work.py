from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
            self,
            exc_type: object | None,
            exc_val: BaseException | None,
            exc_tb: object | None,
    ) -> None:
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
