from fastapi import APIRouter

from dependencies.services import MoviePersonServiceDep
from schemas.movie_person import MoviePersonRead, MoviePersonUpdateReq, MoviePersonCreate

router = APIRouter()


@router.get("/")
async def get_movie_person_associations(
        service: MoviePersonServiceDep,
        skip: int = 0,
        limit: int = 100
) -> list[MoviePersonRead]:
    return await service.get_all(skip, limit)


@router.get("/{movie_person_association_id}")
async def get_movie_person_association(
        movie_person_association_id: int,
        service: MoviePersonServiceDep
) -> MoviePersonRead:
    return await service.get_by_id(movie_person_association_id)


@router.post("/")
async def create_movie_person_association(
        data: MoviePersonCreate,
        service: MoviePersonServiceDep
) -> MoviePersonRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_movie_person_associations(
        data: list[MoviePersonCreate],
        service: MoviePersonServiceDep
) -> list[MoviePersonRead]:
    return await service.bulk_create(data)


@router.patch("/{movie_person_association_id}")
async def update_movie_person_association(
        movie_person_association_id: int,
        data: MoviePersonUpdateReq,
        service: MoviePersonServiceDep
) -> MoviePersonRead:
    return await service.update(movie_person_association_id, data)


@router.delete("/{movie_person_association_id}")
async def delete_movie_person_association(
        movie_person_association_id: int,
        service: MoviePersonServiceDep
) -> None:
    return await service.delete(movie_person_association_id)
