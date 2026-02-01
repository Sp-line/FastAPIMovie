from collections import UserList

from signals.types import AsyncEventFactory


class EventList(UserList[AsyncEventFactory]):
    async def send_all(self) -> None:
        if not self.data:
            return
        for event_factory in self.data:
            await event_factory()
        self.clear()
