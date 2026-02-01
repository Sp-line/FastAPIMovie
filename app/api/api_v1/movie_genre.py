from fastapi import APIRouter

from dependencies.services import MovieGenreServiceDep
from schemas.movie_genre import MovieGenreRead, MovieGenreCreate, MovieGenreUpdate

router = APIRouter()


@router.get("/")
async def get_movie_genre_associations(
        service: MovieGenreServiceDep,
        skip: int = 0,
        limit: int = 100
) -> list[MovieGenreRead]:
    return await service.get_all(skip, limit)


@router.get("/{movie_genre_association_id}")
async def get_movie_genre_association(
        movie_genre_association_id: int,
        service: MovieGenreServiceDep
) -> MovieGenreRead:
    return await service.get_by_id(movie_genre_association_id)


@router.post("/")
async def create_movie_genre_association(
        data: MovieGenreCreate,
        service: MovieGenreServiceDep
) -> MovieGenreRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_movie_genre_associations(
        data: list[MovieGenreCreate],
        service: MovieGenreServiceDep
) -> list[MovieGenreRead]:
    return await service.bulk_create(data)


@router.patch("/{movie_genre_association_id}")
async def update_movie_genre_association(
        movie_genre_association_id: int,
        data: MovieGenreUpdate,
        service: MovieGenreServiceDep
) -> MovieGenreRead:
    return await service.update(
        movie_genre_association_id,
        data
    )


@router.delete("/{movie_genre_association_id}")
async def delete_movie_genre_association(
        movie_genre_association_id: int,
        service: MovieGenreServiceDep
) -> None:
    return await service.delete(movie_genre_association_id)
