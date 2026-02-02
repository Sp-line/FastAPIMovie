from core import fs_router
from schemas.base import Id
from schemas.country import CountryCreateEvent, CountryUpdateEvent
from schemas.event import BaseEventPublishers

country_created = fs_router.publisher(
    "countries.created",
    schema=CountryCreateEvent,
)

country_bulk_created = fs_router.publisher(
    "countries.bulk.created",
    schema=list[CountryCreateEvent],
)

country_updated = fs_router.publisher(
    "countries.updated",
    schema=CountryUpdateEvent,
)

country_deleted = fs_router.publisher(
    "countries.deleted",
    schema=Id,
)

country_base_publishers = BaseEventPublishers(
    create_pub=country_created,
    bulk_create_pub=country_bulk_created,
    update_pub=country_updated,
    delete_pub=country_deleted,
)
