import os
from fastapi import APIRouter
from pathlib import Path
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env01"
load_dotenv(dotenv_path=env_path)
token = os.getenv("site85_token")

router = APIRouter()

@router.get("/")
async def get_users():
    return {
        "message": "유저 목록입니다...", 
        "token": token,
        "current_dir": current_dir, 
    }


