from fastapi import FastAPI
from .routes import fastapi01

app = FastAPI()

app.include_router(fastapi01.router, prefix="/api/fastapi/fastapi01", tags=["fastapi01"])

@app.get("/")
async def root():
    return {"message": "FastAPI 전용 API 루트입니다."}

