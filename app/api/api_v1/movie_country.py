from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from schemas.movie_country import MovieCountryRead, MovieCountryCreate
from services.m2m import MovieCountryService

router = APIRouter(route_class=DishkaRoute)


@router.post("/")
async def create_movie_country_association(
        data: MovieCountryCreate,
        service: FromDishka[MovieCountryService]
) -> MovieCountryRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_movie_country_associations(
        data: list[MovieCountryCreate],
        service: FromDishka[MovieCountryService]
) -> list[MovieCountryRead]:
    return await service.bulk_create(data)


@router.delete("/{movie_country_association_id}")
async def delete_movie_country_association(
        movie_country_association_id: int,
        service: FromDishka[MovieCountryService]
) -> None:
    return await service.delete(movie_country_association_id)
