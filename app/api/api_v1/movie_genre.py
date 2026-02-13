from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Limiter, Rate, Duration

from schemas.movie_genre import MovieGenreRead, MovieGenreCreate
from services.m2m import MovieGenreService

router = APIRouter(route_class=DishkaRoute)


@router.post(
    "/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def create_movie_genre_association(
        data: MovieGenreCreate,
        service: FromDishka[MovieGenreService]
) -> MovieGenreRead:
    return await service.create(data)


@router.post(
    "/bulk",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(5, Duration.MINUTE)))),
    ]
)
async def bulk_create_movie_genre_associations(
        data: list[MovieGenreCreate],
        service: FromDishka[MovieGenreService]
) -> list[MovieGenreRead]:
    return await service.bulk_create(data)


@router.delete(
    "/{movie_genre_association_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def delete_movie_genre_association(
        movie_genre_association_id: int,
        service: FromDishka[MovieGenreService]
) -> None:
    return await service.delete(movie_genre_association_id)
