from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Limiter, Rate, Duration

from schemas.movie_country import MovieCountryRead, MovieCountryCreate
from services.m2m import MovieCountryService

router = APIRouter(route_class=DishkaRoute)


@router.post(
    "/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def create_movie_country_association(
        data: MovieCountryCreate,
        service: FromDishka[MovieCountryService]
) -> MovieCountryRead:
    return await service.create(data)


@router.post(
    "/bulk",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(5, Duration.MINUTE)))),
    ]
)
async def bulk_create_movie_country_associations(
        data: list[MovieCountryCreate],
        service: FromDishka[MovieCountryService]
) -> list[MovieCountryRead]:
    return await service.bulk_create(data)


@router.delete(
    "/{movie_country_association_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def delete_movie_country_association(
        movie_country_association_id: int,
        service: FromDishka[MovieCountryService]
) -> None:
    return await service.delete(movie_country_association_id)
