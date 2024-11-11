from fastapi import APIRouter, HTTPException, status
from schemas.file_schemas import FileCreate, FileUpdate
from services.file_services import FileService


file_router = APIRouter()


@file_router.get("/")
async def get_files_handler():
    try:
        return await FileService.get_files()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@file_router.get("/{file_id}")
async def get_file_by_id_handler(file_id: str):
    try:
        return await FileService.get_file_by_id(file_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@file_router.post("/")
async def create_file_handler(file: FileCreate):
    try:
        return await FileService.create_file(file)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@file_router.put("/{file_id}")
async def update_file_handler(file_id: str, file: FileUpdate):
    try:
        return await FileService.update_file(file_id, file)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@file_router.delete("/{file_id}")
async def delete_file_handler(file_id: str):
    try:
        return await FileService.delete_file(file_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
