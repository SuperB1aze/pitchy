from uuid import uuid4
from urllib.parse import urlparse

from fastapi import HTTPException, UploadFile
from pydantic.json_schema import SkipJsonSchema
from sqlalchemy import select, func

from src.config import settings
from src.database import async_session_factory
from infrastructure.db.models import FormsOrm, MediasOrm
from src.infrastructure.minioS3.minio import S3Client


class MediaServiceORM:
    MAX_FORM_MEDIA_FILES = 10
    ALLOWED_MEDIA_PREFIXES = ("image/", "video/")

    @staticmethod
    def normalize_media_files(
        media_files: list[UploadFile | SkipJsonSchema[str]] | None,
    ) -> list[UploadFile] | None:
        if not media_files:
            return None
        normalized: list[UploadFile] = []
        for media_file in media_files:
            if isinstance(media_file, str):
                if media_file.strip().lower() in {"", "string"}:
                    continue
                raise HTTPException(status_code=422, detail="Invalid media_files value")
            normalized.append(media_file)
        return normalized or None

    @staticmethod
    async def upload_to_minio(
        owner_prefix: str,
        owner_id: int,
        file: UploadFile,
    ) -> str:
        if not file.content_type or not file.content_type.startswith(MediaServiceORM.ALLOWED_MEDIA_PREFIXES):
            raise HTTPException(status_code=400, detail="Only image or video files are allowed")

        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        ext = ""
        if file.filename and "." in file.filename:
            ext = "." + file.filename.rsplit(".", 1)[-1].lower()
        object_name = f"development/{owner_prefix}/{owner_id}/{uuid4().hex}{ext}"

        s3 = S3Client(
            access_key=settings.minio.access_key,
            secret_key=settings.minio.secret_key,
            endpoint_url=settings.minio.endpoint_url,
            bucket_name=settings.minio.bucket_name,
        )
        await s3.upload_bytes(file_bytes, object_name, file.content_type or "application/octet-stream")
        return s3.build_object_url(object_name, settings.minio.endpoint_url)

    @staticmethod
    def extract_obj_name(url: str) -> str | None:
        path = urlparse(url).path.strip("/")
        prefix = f"{settings.minio.bucket_name}/"
        if not path.startswith(prefix):
            return None
        return path.removeprefix(prefix)

    @staticmethod
    async def attach_media(user_id: int, form_id: int, media_files: list[UploadFile] | None) -> None:
        if not media_files:
            return
        if len(media_files) > MediaServiceORM.MAX_FORM_MEDIA_FILES:
            raise HTTPException(status_code=400, detail="You can attach up to 10 media files")

        async with async_session_factory() as session:
            form = await session.get(FormsOrm, form_id)
            if not form:
                raise HTTPException(status_code=404, detail="Form not found")
            if form.user_id != user_id:
                raise HTTPException(status_code=403, detail="You do not have permission to change this form")
            existing_media_count = await session.scalar(
                select(func.count(MediasOrm.id)).where(MediasOrm.form_id == form_id)
            )
            if (existing_media_count or 0) + len(media_files) > MediaServiceORM.MAX_FORM_MEDIA_FILES:
                raise HTTPException(status_code=400, detail="A form can have up to 10 media files in total")

            for media_file in media_files:
                media_url = await MediaServiceORM.upload_to_minio(
                    "forms",
                    form_id,
                    media_file,
                )
                session.add(MediasOrm(filepath=media_url, form_id=form_id))

            await session.commit()

    @staticmethod
    async def clear_form_media(user_id: int, form_id: int) -> None:
        async with async_session_factory() as session:
            form = await session.get(FormsOrm, form_id)
            if not form:
                raise HTTPException(status_code=404, detail="Form not found")
            if form.user_id != user_id:
                raise HTTPException(status_code=403, detail="You do not have permission to change this form")

            medias = await session.scalars(select(MediasOrm).where(MediasOrm.form_id == form_id))
            media_list = list(medias.all())
            for media in media_list:
                await session.delete(media)
            await session.commit()

        s3 = S3Client(
            access_key=settings.minio.access_key,
            secret_key=settings.minio.secret_key,
            endpoint_url=settings.minio.endpoint_url,
            bucket_name=settings.minio.bucket_name,
        )
        for media in media_list:
            object_name = MediaServiceORM.extract_obj_name(media.filepath)
            if object_name is None:
                continue
            try:
                await s3.delete_object(object_name)
            except Exception:
                continue