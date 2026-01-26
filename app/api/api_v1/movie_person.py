from fastapi import APIRouter

from dependencies.services import MoviePersonServiceDep
from schemas.movie_person import MoviePersonRead, MoviePersonCompositeId, MoviePersonUpdate, MoviePersonCreate

router = APIRouter()


@router.get("/movie-person-associations")
async def get_movie_person_associations(
        service: MoviePersonServiceDep,
        skip: int = 0,
        limit: int = 100
) -> list[MoviePersonRead]:
    return await service.get_all(skip, limit)


@router.get("/movies/{movie_id}/persons/{person_id}")
async def get_movie_person_association(
        movie_id: int,
        person_id: int,
        service: MoviePersonServiceDep
) -> MoviePersonRead:
    return await service.get_by_id(MoviePersonCompositeId(person_id=person_id, movie_id=movie_id))


@router.post("/movies/{movie_id}/persons/{person_id}")
async def create_movie_person_association(
        movie_id: int,
        person_id: int,
        data: MoviePersonCreate,
        service: MoviePersonServiceDep
) -> MoviePersonRead:
    return await service.create(
        MoviePersonCreate(
            movie_id=movie_id,
            person_id=person_id,
            **data.model_dump()
        )
    )


@router.post("/movie-person-associations/bulk")
async def bulk_create_movie_person_associations(
        data: list[MoviePersonCreate],
        service: MoviePersonServiceDep
) -> list[MoviePersonRead]:
    return await service.bulk_create(data)


@router.patch("/movies/{movie_id}/persons/{person_id}")
async def update_movie_person_association(
        movie_id: int,
        person_id: int,
        data: MoviePersonUpdate,
        service: MoviePersonServiceDep
) -> MoviePersonRead:
    return await service.update(
        MoviePersonCompositeId(movie_id=movie_id, person_id=person_id),
        data
    )


@router.delete("/movies/{movie_id}/persons/{person_id}")
async def delete_movie_person_association(
        movie_id: int,
        person_id: int,
        service: MoviePersonServiceDep
) -> None:
    return await service.delete(MoviePersonCompositeId(person_id=person_id, movie_id=movie_id))
