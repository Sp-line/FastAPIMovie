from fastapi import APIRouter, UploadFile

from dependencies.services import MovieServiceDep, MovieFileServiceDep
from schemas.movie import MovieList, MovieRead, MovieCreateReq, MovieUpdateReq, MovieDetail

router = APIRouter()


@router.get("/")
async def get_movies(service: MovieServiceDep, skip: int = 0, limit: int = 100) -> list[MovieList]:
    return await service.get_all(skip, limit)


@router.get("/{movie_id}")
async def get_movie(movie_id: int, service: MovieServiceDep) -> MovieDetail:
    return await service.get_by_id(movie_id)


@router.post("/")
async def create_movie(data: MovieCreateReq, service: MovieServiceDep) -> MovieRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_movies(data: list[MovieCreateReq], service: MovieServiceDep) -> list[MovieRead]:
    return await service.bulk_create(data)


@router.patch("/{movie_id}")
async def update_movie(movie_id: int, data: MovieUpdateReq, service: MovieServiceDep) -> MovieRead:
    return await service.update(movie_id, data)


@router.put("/{movie_id}/posters")
async def update_movie_poster(movie_id: int, poster: UploadFile, service: MovieFileServiceDep) -> MovieRead:
    return await service.save(movie_id, poster)


@router.delete("/{movie_id}/posters")
async def delete_movie_poster(movie_id: int, service: MovieFileServiceDep) -> MovieRead:
    return await service.delete(movie_id)


@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, service: MovieServiceDep) -> None:
    return await service.delete(movie_id)
