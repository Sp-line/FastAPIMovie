from fastapi import APIRouter, UploadFile

from dependencies.services import MovieShotServiceDep, MovieShotFileServiceDep
from schemas.movie_shot import MovieShotCreateReq, MovieShotUpdateReq, MovieShotRead

router = APIRouter()


@router.get("/")
async def get_movie_shots(service: MovieShotServiceDep) -> list[MovieShotRead]:
    return await service.get_all()


@router.get("/{movie_shot_id}")
async def get_movie_shot(movie_shot_id: int, service: MovieShotServiceDep) -> MovieShotRead:
    return await service.get_by_id(movie_shot_id)


@router.post("/")
async def create_movie_shot(data: MovieShotCreateReq, service: MovieShotServiceDep) -> MovieShotRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_movie_shots(data: list[MovieShotCreateReq], service: MovieShotServiceDep) -> list[MovieShotRead]:
    return await service.bulk_create(data)


@router.patch("/{movie_shot_id}")
async def update_movie_shot(movie_shot_id: int, data: MovieShotUpdateReq, service: MovieShotServiceDep) -> MovieShotRead:
    return await service.update(movie_shot_id, data)


@router.put("/{movie_shot_id}/images")
async def update_movie_shot_image(movie_shot_id: int, image: UploadFile, service: MovieShotFileServiceDep) -> MovieShotRead:
    return await service.update_file(movie_shot_id, image)


@router.delete("/{movie_shot_id}")
async def delete_movie_shot(movie_shot_id: int, service: MovieShotServiceDep) -> None:
    return await service.delete(movie_shot_id)