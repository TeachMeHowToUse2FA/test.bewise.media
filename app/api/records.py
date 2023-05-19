import uuid

from pathlib import Path

from fastapi import APIRouter, UploadFile, Request, HTTPException, status
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.dependencies import convert_media
from app.db.base import database, users, records


router = APIRouter(tags=["records"])


@router.post("/records", tags=["records"], status_code=status.HTTP_201_CREATED)
async def upload_record(request: Request, file: UploadFile, user_id: uuid.UUID, token: str):
    if file.content_type not in ["audio/wav", "audio/x-wav"]:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Only WAV files are allowed")
    
    query = users.select().where(users.c.id == user_id)
    user_db = await database.fetch_one(query)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user_db['token'] != token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token invalid")
    
    filename = await convert_media(file)

    query = records.insert().values(user_id=user_id, filename=filename)
    record_id = await database.execute(query)

    return {"file": f"{request.base_url}record?id={record_id}&user={user_id}"}


@router.get("/record", response_class=FileResponse)
async def get_record(id: uuid.UUID, user: uuid.UUID):
    query = records.select().where(records.c.id == id)
    record_db = await database.fetch_one(query)

    if not record_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found or removed")
    
    if user != record_db["user_id"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can not view this file")
        
    filepath = Path(settings.STORAGE_DIR).joinpath(record_db["filename"])
    
    return filepath
