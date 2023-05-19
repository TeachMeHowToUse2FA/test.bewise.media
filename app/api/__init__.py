from fastapi import APIRouter

from app.api import users, records


router = APIRouter()

router.include_router(users.router)
router.include_router(records.router)
