from typing import TypeVar

from repositories.base import RepositoryBase

RepositoryBaseType = TypeVar("RepositoryBaseType", bound=RepositoryBase)
