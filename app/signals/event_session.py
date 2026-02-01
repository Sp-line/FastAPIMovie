from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from signals.event_list import EventList


class EventSession(AsyncSession):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.events = EventList()