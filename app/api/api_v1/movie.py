from typing import Annotated

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, UploadFile, Query, Depends
from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Limiter, Rate, Duration

from schemas.movie import MovieList, MovieRead, MovieCreateReq, MovieUpdateReq, MovieDetail, MovieSearchRead, \
    MovieFilter
from services.movie import MovieSearchService, MovieFilterService, MovieService, MovieFileService

router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/search",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(20, Duration.MINUTE)))),
    ]
)
async def search_movie(
        service: FromDishka[MovieSearchService],
        query: str,
        skip: int = 0,
        limit: int = 10
) -> list[MovieSearchRead]:
    return await service.search(query, skip, limit)


@router.get(
    "/filter",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(20, Duration.MINUTE)))),
    ]
)
async def filter_movies(
        service: FromDishka[MovieFilterService],
        filters: Annotated[MovieFilter, Query()]
) -> list[MovieRead]:
    return await service.get(filters)


@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(120, Duration.MINUTE)))),
    ]
)
async def get_movies(service: FromDishka[MovieService], skip: int = 0, limit: int = 100) -> list[MovieRead]:
    return await service.get_all(skip, limit)


@router.get(
    "/{movie_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(120, Duration.MINUTE)))),
    ]
)
async def get_movie(movie_id: int, service: FromDishka[MovieService]) -> MovieRead:
    return await service.get_by_id(movie_id)


@router.get(
    "/list/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(120, Duration.MINUTE)))),
    ]
)
async def get_movies_for_list(service: FromDishka[MovieService], skip: int = 0, limit: int = 100) -> list[MovieList]:
    return await service.get_for_list(skip, limit)


@router.get(
    "/detail/{movie_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(120, Duration.MINUTE)))),
    ]
)
async def get_movie_for_detail(movie_id: int, service: FromDishka[MovieService]) -> MovieDetail:
    return await service.get_for_detail(movie_id)


@router.post(
    "/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def create_movie(data: MovieCreateReq, service: FromDishka[MovieService]) -> MovieRead:
    return await service.create(data)


@router.post(
    "/bulk",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(5, Duration.MINUTE)))),
    ]
)
async def bulk_create_movies(data: list[MovieCreateReq], service: FromDishka[MovieService]) -> list[MovieRead]:
    return await service.bulk_create(data)


@router.patch(
    "/{movie_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def update_movie(movie_id: int, data: MovieUpdateReq, service: FromDishka[MovieService]) -> MovieRead:
    return await service.update(movie_id, data)


@router.put(
    "/{movie_id}/posters",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(5, Duration.MINUTE)))),
    ]
)
async def update_movie_poster(movie_id: int, poster: UploadFile, service: FromDishka[MovieFileService]) -> MovieRead:
    return await service.save(movie_id, poster)


@router.delete(
    "/{movie_id}/posters",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def delete_movie_poster(movie_id: int, service: FromDishka[MovieFileService]) -> MovieRead:
    return await service.delete(movie_id)


@router.delete(
    "/{movie_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def delete_movie(movie_id: int, service: FromDishka[MovieService]) -> None:
    return await service.delete(movie_id)
