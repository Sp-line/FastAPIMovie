from typing import NewType

from cache.invalidator import CacheInvalidatorBase

CountryCacheInvalidator = NewType("CountryCacheInvalidator", CacheInvalidatorBase)
GenreCacheInvalidator = NewType("GenreCacheInvalidator", CacheInvalidatorBase)
PersonCacheInvalidator = NewType("PersonCacheInvalidator", CacheInvalidatorBase)
MoviePersonCacheInvalidator = NewType("MoviePersonCacheInvalidator", CacheInvalidatorBase)
