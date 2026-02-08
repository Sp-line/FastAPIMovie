from fastapi import APIRouter

from schemas.country import CountryRead, CountryCreateReq, CountryUpdateReq, CountrySearchRead
from services.country import CountrySearchService, CountryService
from dishka.integrations.fastapi import FromDishka, DishkaRoute

router = APIRouter(route_class=DishkaRoute)


@router.get("/search")
async def search_country(
        service: FromDishka[CountrySearchService],
        query: str,
        skip: int = 0,
        limit: int = 10
) -> list[CountrySearchRead]:
    return await service.search(query, skip, limit)


@router.get("/")
async def get_countries(service: FromDishka[CountryService], skip: int = 0, limit: int = 100) -> list[CountryRead]:
    return await service.get_all(skip, limit)


@router.get("/{country_id}")
async def get_country(country_id: int, service: FromDishka[CountryService]) -> CountryRead:
    return await service.get_by_id(country_id)


@router.post("/")
async def create_country(data: CountryCreateReq, service: FromDishka[CountryService]) -> CountryRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_countries(data: list[CountryCreateReq], service: FromDishka[CountryService]) -> list[CountryRead]:
    return await service.bulk_create(data)


@router.patch("/{country_id}")
async def update_country(country_id: int, data: CountryUpdateReq, service: FromDishka[CountryService]) -> CountryRead:
    return await service.update(country_id, data)


@router.delete("/{country_id}")
async def delete_country(country_id: int, service: FromDishka[CountryService]) -> None:
    return await service.delete(country_id)
