from fastapi import APIRouter

from dependencies.services import MovieGenreServiceDep
from schemas.movie_genre import MovieGenreCompositeId, MovieGenreRead, MovieGenreCreate, MovieGenreUpdate

router = APIRouter()


@router.get("/movie-genre-associations")
async def get_movie_genre_associations(
        service: MovieGenreServiceDep
) -> list[MovieGenreRead]:
    return await service.get_all()


@router.get("/movies/{movie_id}/genres/{genre_id}")
async def get_movie_genre_association(
        movie_id: int,
        genre_id: int,
        service: MovieGenreServiceDep
) -> MovieGenreRead:
    return await service.get_by_id(MovieGenreCompositeId(genre_id=genre_id, movie_id=movie_id))


@router.post("/movies/{movie_id}/genres/{genre_id}")
async def create_movie_genre_association(
        movie_id: int,
        genre_id: int,
        service: MovieGenreServiceDep
) -> MovieGenreRead:
    return await service.create(MovieGenreCreate(movie_id=movie_id, genre_id=genre_id))


@router.post("/movie-genre-associations/bulk")
async def bulk_create_movie_genre_associations(
        data: list[MovieGenreCreate],
        service: MovieGenreServiceDep
) -> list[MovieGenreRead]:
    return await service.bulk_create(data)


@router.patch("/movies/{movie_id}/genres/{genre_id}")
async def update_movie_genre_association(
        movie_id: int,
        genre_id: int,
        data: MovieGenreUpdate,
        service: MovieGenreServiceDep
) -> MovieGenreRead:
    return await service.update(
        MovieGenreCompositeId(movie_id=movie_id, genre_id=genre_id),
        data
    )


@router.delete("/movies/{movie_id}/genres/{genre_id}")
async def delete_movie_genre_association(
        movie_id: int,
        genre_id: int,
        service: MovieGenreServiceDep
) -> None:
    return await service.delete(MovieGenreCompositeId(genre_id=genre_id, movie_id=movie_id))