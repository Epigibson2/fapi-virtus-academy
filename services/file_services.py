from models.files_model import File
from schemas.file_schemas import FileCreate, FileResponse, FileUpdate


class FileService:

    @staticmethod
    async def get_files() -> list[FileResponse]:
        files = await File.find_all().to_list()
        for file in files:
            await file.fetch_link(file.owner)
        return files

    @staticmethod
    async def get_file_by_id(file_id: str) -> FileResponse:
        file = await File.find_one(File.id == file_id)
        await file.fetch_link(file.owner)
        return file

    @staticmethod
    async def create_file(file: FileCreate) -> FileResponse:
        file = File(**file.model_dump())
        await file.insert()
        await file.fetch_link(file.owner)
        return file

    @staticmethod
    async def update_file(file_id: str, file: FileUpdate) -> FileResponse:
        file = await FileService.get_file_by_id(file_id)
        await file.update({"set": file.model_dump(exclude_unset=True)})
        await file.fetch_link(file.owner)
        return file

    @staticmethod
    async def delete_file(file_id: str) -> None:
        file = await FileService.get_file_by_id(file_id)
        await file.update({"set": {"is_deleted": True}})
        await file.fetch_link(file.owner)
        return file
