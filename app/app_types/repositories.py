from typing import TypeVar

from repositories.base import RepositoryBase, M2MRepositoryBase

RepositoryBaseType = TypeVar("RepositoryBaseType", bound=RepositoryBase)
M2MRepositoryBaseType = TypeVar("M2MRepositoryBaseType", bound=M2MRepositoryBase)
