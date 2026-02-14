from typing import Annotated

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, UploadFile, Depends
from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Limiter, Rate, Duration

from dependencies.files import validate_image_file
from schemas.movie_shot import MovieShotCreateReq, MovieShotUpdateReq, MovieShotRead
from services.movie_shot import MovieShotService, MovieShotFileService

router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(120, Duration.MINUTE)))),
    ]
)
async def get_movie_shots(service: FromDishka[MovieShotService], skip: int = 0, limit: int = 100) -> list[
    MovieShotRead]:
    return await service.get_all(skip, limit)


@router.get(
    "/{movie_shot_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(120, Duration.MINUTE)))),
    ]
)
async def get_movie_shot(movie_shot_id: int, service: FromDishka[MovieShotService]) -> MovieShotRead:
    return await service.get_by_id(movie_shot_id)


@router.post(
    "/",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def create_movie_shot(data: MovieShotCreateReq, service: FromDishka[MovieShotService]) -> MovieShotRead:
    return await service.create(data)


@router.post(
    "/bulk",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(5, Duration.MINUTE)))),
    ]
)
async def bulk_create_movie_shots(data: list[MovieShotCreateReq], service: FromDishka[MovieShotService]) -> list[
    MovieShotRead]:
    return await service.bulk_create(data)


@router.patch(
    "/{movie_shot_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def update_movie_shot(movie_shot_id: int, data: MovieShotUpdateReq,
                            service: FromDishka[MovieShotService]) -> MovieShotRead:
    return await service.update(movie_shot_id, data)


@router.put(
    "/{movie_shot_id}/images",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(5, Duration.MINUTE)))),
    ]
)
async def update_movie_shot_image(
        movie_shot_id: int,
        image: Annotated[UploadFile, Depends(validate_image_file)],
        service: FromDishka[MovieShotFileService]
) -> MovieShotRead:
    return await service.save(movie_shot_id, image)


@router.delete(
    "/{movie_shot_id}/images",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def delete_movie_shot_image(movie_shot_id: int, service: FromDishka[MovieShotFileService]) -> MovieShotRead:
    return await service.delete(movie_shot_id)


@router.delete(
    "/{movie_shot_id}",
    dependencies=[
        Depends(RateLimiter(limiter=Limiter(Rate(30, Duration.MINUTE)))),
    ]
)
async def delete_movie_shot(movie_shot_id: int, service: FromDishka[MovieShotService]) -> None:
    return await service.delete(movie_shot_id)
