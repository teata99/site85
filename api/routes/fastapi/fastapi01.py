import os
from fastapi import APIRouter

token = os.environ.get("site85_token")

router = APIRouter()

@router.get("/")
async def get_users():
    return {"message": "유저 목록입니다.", "token:": token}
