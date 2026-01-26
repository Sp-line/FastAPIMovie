from fastapi import APIRouter, UploadFile

from dependencies.services import PersonServiceDep, PersonFileServiceDep
from schemas.person import PersonUpdateReq, PersonCreateReq, PersonRead

router = APIRouter()


@router.get("/")
async def get_persons(service: PersonServiceDep) -> list[PersonRead]:
    return await service.get_all()


@router.get("/{person_id}")
async def get_person(person_id: int, service: PersonServiceDep) -> PersonRead:
    return await service.get_by_id(person_id)


@router.post("/")
async def create_person(data: PersonCreateReq, service: PersonServiceDep) -> PersonRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_persons(data: list[PersonCreateReq], service: PersonServiceDep) -> list[PersonRead]:
    return await service.bulk_create(data)


@router.patch("/{person_id}")
async def update_person(person_id: int, data: PersonUpdateReq, service: PersonServiceDep) -> PersonRead:
    return await service.update(person_id, data)


@router.put("/{person_id}/photos")
async def update_person_photo(person_id: int, photo: UploadFile, service: PersonFileServiceDep) -> PersonRead:
    return await service.save(person_id, photo)


@router.delete("/{person_id}")
async def delete_person(person_id: int, service: PersonServiceDep) -> None:
    return await service.delete(person_id)
