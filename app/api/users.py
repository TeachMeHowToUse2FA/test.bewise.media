import uuid

from fastapi import APIRouter, status

from app.db.base import database, users
from app.schemas.user import UserIn


router = APIRouter(tags=["users"])


@router.post("/users", tags=["users"], status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn):
    token = uuid.uuid4().hex

    query = users.insert().values(username=user.username, token=token)
    user_id = await database.execute(query)

    return {"user_id": user_id, "token": token}
