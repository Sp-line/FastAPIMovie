from fastapi import APIRouter

from dependencies.services import GenreServiceDep, GenreSearchServiceDep
from schemas.genre import GenreRead, GenreUpdateReq, GenreCreateReq, GenreSearchRead

router = APIRouter()


@router.get("/search")
async def search_genre(
        service: GenreSearchServiceDep,
        query: str,
        skip: int = 0,
        limit: int = 10
) -> list[GenreSearchRead]:
    return await service.search(query, skip, limit)


@router.get("/")
async def get_genres(service: GenreServiceDep, skip: int = 0, limit: int = 100) -> list[GenreRead]:
    return await service.get_all(skip, limit)


@router.get("/{genre_id}")
async def get_genre(genre_id: int, service: GenreServiceDep) -> GenreRead:
    return await service.get_by_id(genre_id)


@router.post("/")
async def create_genre(data: GenreCreateReq, service: GenreServiceDep) -> GenreRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_genres(data: list[GenreCreateReq], service: GenreServiceDep) -> list[GenreRead]:
    return await service.bulk_create(data)


@router.patch("/{genre_id}")
async def update_genre(genre_id: int, data: GenreUpdateReq, service: GenreServiceDep) -> GenreRead:
    return await service.update(genre_id, data)


@router.delete("/{genre_id}")
async def delete_genre(genre_id: int, service: GenreServiceDep) -> None:
    return await service.delete(genre_id)
