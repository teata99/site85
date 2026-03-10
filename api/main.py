import os
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from .routes.fastapi import fastapi01
from .routes.fastapi import fastapi02
from .routes.fastapi import fastapi03

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(fastapi01.router, prefix="/api/fastapi/fastapi01", tags=["fastapi01"])
app.include_router(fastapi02.router, prefix="/api/fastapi/fastapi02", tags=["fastapi02"])
app.include_router(fastapi03.router, prefix="/api/fastapi/fastapi03", tags=["fastapi03"])


@app.get("/")
async def root():
    return {"message": "FastAPI 전용 API 루트입니다."}


