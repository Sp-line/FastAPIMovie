from typing import TypeAlias, Callable, Awaitable

AsyncEventFactory: TypeAlias = Callable[[], Awaitable[None]]
