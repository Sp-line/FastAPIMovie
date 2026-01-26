from fastapi import APIRouter

from dependencies.services import MovieCountryServiceDep
from schemas.movie_country import MovieCountryRead, MovieCountryCompositeId, MovieCountryCreate, MovieCountryUpdate

router = APIRouter()


@router.get("/movie-country-associations")
async def get_movie_country_associations(
        service: MovieCountryServiceDep,
        skip: int = 0,
        limit: int = 100
) -> list[MovieCountryRead]:
    return await service.get_all(skip, limit)


@router.get("/movies/{movie_id}/countries/{country_id}")
async def get_movie_country_association(
        movie_id: int,
        country_id: int,
        service: MovieCountryServiceDep
) -> MovieCountryRead:
    return await service.get_by_id(MovieCountryCompositeId(country_id=country_id, movie_id=movie_id))


@router.post("/movies/{movie_id}/countries/{country_id}")
async def create_movie_country_association(
        movie_id: int,
        country_id: int,
        service: MovieCountryServiceDep
) -> MovieCountryRead:
    return await service.create(MovieCountryCreate(movie_id=movie_id, country_id=country_id))


@router.post("/movie-country-associations/bulk")
async def bulk_create_movie_country_associations(
        data: list[MovieCountryCreate],
        service: MovieCountryServiceDep
) -> list[MovieCountryRead]:
    return await service.bulk_create(data)


@router.patch("/movies/{movie_id}/countries/{country_id}")
async def update_movie_country_association(
        movie_id: int,
        country_id: int,
        data: MovieCountryUpdate,
        service: MovieCountryServiceDep
) -> MovieCountryRead:
    return await service.update(
        MovieCountryCreate(movie_id=movie_id, country_id=country_id),
        data
    )


@router.delete("/movies/{movie_id}/countries/{country_id}")
async def delete_movie_country_association(
        movie_id: int,
        country_id: int,
        service: MovieCountryServiceDep
) -> None:
    return await service.delete(MovieCountryCompositeId(country_id=country_id, movie_id=movie_id))
