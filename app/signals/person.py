from core import fs_router
from schemas.base import Id
from schemas.event import BaseEventPublishers
from schemas.person import PersonCreateEvent, PersonUpdateEvent

person_created = fs_router.publisher(
    "persons.created",
    schema=PersonCreateEvent,
)

person_bulk_created = fs_router.publisher(
    "persons.bulk.created",
    schema=list[PersonCreateEvent],
)

person_updated = fs_router.publisher(
    "persons.updated",
    schema=PersonUpdateEvent,
)

person_deleted = fs_router.publisher(
    "persons.deleted",
    schema=Id,
)

person_base_publishers = BaseEventPublishers(
    create_pub=person_created,
    bulk_create_pub=person_bulk_created,
    update_pub=person_updated,
    delete_pub=person_deleted,
)
