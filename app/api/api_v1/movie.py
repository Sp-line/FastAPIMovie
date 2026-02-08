from typing import Annotated

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, UploadFile, Query

from schemas.movie import MovieList, MovieRead, MovieCreateReq, MovieUpdateReq, MovieDetail, MovieSearchRead, \
    MovieFilter
from services.movie import MovieSearchService, MovieFilterService, MovieService, MovieFileService

router = APIRouter(route_class=DishkaRoute)


@router.get("/search")
async def search_movie(
        service: FromDishka[MovieSearchService],
        query: str,
        skip: int = 0,
        limit: int = 10
) -> list[MovieSearchRead]:
    return await service.search(query, skip, limit)


@router.get("/filter")
async def filter_movies(
        service: FromDishka[MovieFilterService],
        filters: Annotated[MovieFilter, Query()]
) -> list[MovieRead]:
    return await service.get(filters)


@router.get("/")
async def get_movies(service: FromDishka[MovieService], skip: int = 0, limit: int = 100) -> list[MovieRead]:
    return await service.get_all(skip, limit)


@router.get("/{movie_id}")
async def get_movie(movie_id: int, service: FromDishka[MovieService]) -> MovieRead:
    return await service.get_by_id(movie_id)


@router.get("/list/")
async def get_movies_for_list(service: FromDishka[MovieService], skip: int = 0, limit: int = 100) -> list[MovieList]:
    return await service.get_for_list(skip, limit)


@router.get("/detail/{movie_id}")
async def get_movie_for_detail(movie_id: int, service: FromDishka[MovieService]) -> MovieDetail:
    return await service.get_for_detail(movie_id)


@router.post("/")
async def create_movie(data: MovieCreateReq, service: FromDishka[MovieService]) -> MovieRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_movies(data: list[MovieCreateReq], service: FromDishka[MovieService]) -> list[MovieRead]:
    return await service.bulk_create(data)


@router.patch("/{movie_id}")
async def update_movie(movie_id: int, data: MovieUpdateReq, service: FromDishka[MovieService]) -> MovieRead:
    return await service.update(movie_id, data)


@router.put("/{movie_id}/posters")
async def update_movie_poster(movie_id: int, poster: UploadFile, service: FromDishka[MovieFileService]) -> MovieRead:
    return await service.save(movie_id, poster)


@router.delete("/{movie_id}/posters")
async def delete_movie_poster(movie_id: int, service: FromDishka[MovieFileService]) -> MovieRead:
    return await service.delete(movie_id)


@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, service: FromDishka[MovieService]) -> None:
    return await service.delete(movie_id)
