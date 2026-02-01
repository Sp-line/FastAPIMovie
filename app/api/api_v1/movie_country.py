from fastapi import APIRouter

from dependencies.services import MovieCountryServiceDep
from schemas.movie_country import MovieCountryRead, MovieCountryCreate, MovieCountryUpdate

router = APIRouter()


@router.get("/")
async def get_movie_country_associations(
        service: MovieCountryServiceDep,
        skip: int = 0,
        limit: int = 100
) -> list[MovieCountryRead]:
    return await service.get_all(skip, limit)


@router.get("/{movie_country_association_id}")
async def get_movie_country_association(
        movie_country_association_id: int,
        service: MovieCountryServiceDep
) -> MovieCountryRead:
    return await service.get_by_id(movie_country_association_id)


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


@router.patch("/{movie_country_association_id}")
async def update_movie_country_association(
        movie_country_association_id: int,
        data: MovieCountryUpdate,
        service: MovieCountryServiceDep
) -> MovieCountryRead:
    return await service.update(
        movie_country_association_id,
        data
    )


@router.delete("/{movie_country_association_id}")
async def delete_movie_country_association(
        movie_country_association_id: int,
        service: MovieCountryServiceDep
) -> None:
    return await service.delete(movie_country_association_id)
