from typing import Annotated

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, UploadFile, Depends
from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Limiter, Rate, Duration

from dependencies.files import validate_image_file
from schemas.person import PersonUpdateReq, PersonCreateReq, PersonRead, PersonSearchRead
from services.person import PersonSearchService, PersonService, PersonFileService

router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/search",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(20, Duration.MINUTE)))),
    ]
)
async def search_person(
        service: FromDishka[PersonSearchService],
        query: str,
        skip: int = 0,
        limit: int = 10
) -> list[PersonSearchRead]:
    return await service.search(query, skip, limit)


@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(120, Duration.MINUTE)))),
    ]
)
async def get_persons(service: FromDishka[PersonService], skip: int = 0, limit: int = 100) -> list[PersonRead]:
    return await service.get_all(skip, limit)


@router.get(
    "/{person_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(120, Duration.MINUTE)))),
    ]
)
async def get_person(person_id: int, service: FromDishka[PersonService]) -> PersonRead:
    return await service.get_by_id(person_id)


@router.post(
    "/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def create_person(data: PersonCreateReq, service: FromDishka[PersonService]) -> PersonRead:
    return await service.create(data)


@router.post(
    "/bulk",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(5, Duration.MINUTE)))),
    ]
)
async def bulk_create_persons(data: list[PersonCreateReq], service: FromDishka[PersonService]) -> list[PersonRead]:
    return await service.bulk_create(data)


@router.patch(
    "/{person_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def update_person(person_id: int, data: PersonUpdateReq, service: FromDishka[PersonService]) -> PersonRead:
    return await service.update(person_id, data)


@router.put(
    "/{person_id}/photos",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(5, Duration.MINUTE)))),
    ]
)
async def update_person_photo(
        person_id: int,
        photo: Annotated[UploadFile, Depends(validate_image_file)],
        service: FromDishka[PersonFileService]
) -> PersonRead:
    return await service.save(person_id, photo)


@router.delete(
    "/{person_id}/photos",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def delete_person_photo(person_id: int, service: FromDishka[PersonFileService]) -> PersonRead:
    return await service.delete(person_id)


@router.delete(
    "/{person_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def delete_person(person_id: int, service: FromDishka[PersonService]) -> None:
    return await service.delete(person_id)
