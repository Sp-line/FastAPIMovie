from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter

from schemas.genre import GenreRead, GenreUpdateReq, GenreCreateReq, GenreSearchRead
from services.genre import GenreSearchService, GenreService

router = APIRouter(route_class=DishkaRoute)


@router.get("/search")
async def search_genre(
        service: FromDishka[GenreSearchService],
        query: str,
        skip: int = 0,
        limit: int = 10
) -> list[GenreSearchRead]:
    return await service.search(query, skip, limit)


@router.get("/")
async def get_genres(service: FromDishka[GenreService], skip: int = 0, limit: int = 100) -> list[GenreRead]:
    return await service.get_all(skip, limit)


@router.get("/{genre_id}")
async def get_genre(genre_id: int, service: FromDishka[GenreService]) -> GenreRead:
    return await service.get_by_id(genre_id)


@router.post("/")
async def create_genre(data: GenreCreateReq, service: FromDishka[GenreService]) -> GenreRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_genres(data: list[GenreCreateReq], service: FromDishka[GenreService]) -> list[GenreRead]:
    return await service.bulk_create(data)


@router.patch("/{genre_id}")
async def update_genre(genre_id: int, data: GenreUpdateReq, service: FromDishka[GenreService]) -> GenreRead:
    return await service.update(genre_id, data)


@router.delete("/{genre_id}")
async def delete_genre(genre_id: int, service: FromDishka[GenreService]) -> None:
    return await service.delete(genre_id)
