from fastapi import APIRouter

from dependencies.services import MovieCountryServiceDep
from schemas.movie_country import MovieCountryRead, MovieCountryCreate, MovieCountryUpdate

router = APIRouter()


@router.post("/")
async def create_movie_country_association(
        data: MovieCountryCreate,
        service: MovieCountryServiceDep
) -> MovieCountryRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_movie_country_associations(
        data: list[MovieCountryCreate],
        service: MovieCountryServiceDep
) -> list[MovieCountryRead]:
    return await service.bulk_create(data)


@router.delete("/{movie_country_association_id}")
async def delete_movie_country_association(
        movie_country_association_id: int,
        service: MovieCountryServiceDep
) -> None:
    return await service.delete(movie_country_association_id)
