from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Limiter, Rate, Duration

from schemas.movie_person import MoviePersonRead, MoviePersonUpdateReq, MoviePersonCreate
from services.m2m import MoviePersonService

router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(120, Duration.MINUTE)))),
    ]
)
async def get_movie_person_associations(
        service: FromDishka[MoviePersonService],
        skip: int = 0,
        limit: int = 100
) -> list[MoviePersonRead]:
    return await service.get_all(skip, limit)


@router.get(
    "/{movie_person_association_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(120, Duration.MINUTE)))),
    ]
)
async def get_movie_person_association(
        movie_person_association_id: int,
        service: FromDishka[MoviePersonService]
) -> MoviePersonRead:
    return await service.get_by_id(movie_person_association_id)


@router.post(
    "/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def create_movie_person_association(
        data: MoviePersonCreate,
        service: FromDishka[MoviePersonService]
) -> MoviePersonRead:
    return await service.create(data)


@router.post(
    "/bulk",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(5, Duration.MINUTE)))),
    ]
)
async def bulk_create_movie_person_associations(
        data: list[MoviePersonCreate],
        service: FromDishka[MoviePersonService]
) -> list[MoviePersonRead]:
    return await service.bulk_create(data)


@router.patch(
    "/{movie_person_association_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def update_movie_person_association(
        movie_person_association_id: int,
        data: MoviePersonUpdateReq,
        service: FromDishka[MoviePersonService]
) -> MoviePersonRead:
    return await service.update(movie_person_association_id, data)


@router.delete(
    "/{movie_person_association_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def delete_movie_person_association(
        movie_person_association_id: int,
        service: FromDishka[MoviePersonService]
) -> None:
    return await service.delete(movie_person_association_id)
