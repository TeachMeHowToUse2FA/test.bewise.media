import aiofiles
import uuid

from fastapi import UploadFile, HTTPException, status

from pathlib import Path
from pydub import AudioSegment

from app.core.config import settings


async def convert_media(file: UploadFile) -> str:
    content = await file.read()

    temp = Path(settings.STORAGE_DIR).joinpath(file.filename)

    async with aiofiles.open(temp, 'wb') as f:
        await f.write(content)

    try:
        audio = AudioSegment.from_file(temp, format="wav")
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid audio file")

    filename = f'{uuid.uuid4().hex}.mp3'
    filepath = Path(settings.STORAGE_DIR).joinpath(filename)

    try:
        audio.export(filepath, format="mp3")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    Path(temp).unlink(missing_ok=True)

    return filename
