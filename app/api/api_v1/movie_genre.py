from fastapi import APIRouter

from dependencies.services import MovieGenreServiceDep
from schemas.movie_genre import MovieGenreRead, MovieGenreCreate, MovieGenreUpdate

router = APIRouter()


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


@router.delete("/{movie_genre_association_id}")
async def delete_movie_genre_association(
        movie_genre_association_id: int,
        service: MovieGenreServiceDep
) -> None:
    return await service.delete(movie_genre_association_id)
