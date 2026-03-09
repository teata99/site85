import os
from fastapi import APIRouter, Depends
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env02"
load_dotenv(dotenv_path=env_path)

router = APIRouter()

class Database:
    def __init__(self):
        self.db_url = os.getenv("POSTGRES_URL")

        if self.db_url and self.db_url.startswith("postgres://"):
            self.db_url = self.db_url.replace("postgres://", "postgresql://", 1)

        if not self.db_url:
            raise ValueError("POSTGRES_URL 환경 변수가 설정되지 않았습니다.")
        
        self.engine = create_engine(self.db_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_instance = Database()

class TestTable(db_instance.Base):
    __tablename__ = "test_connection"
    id = Column(Integer, primary_key=True, index=True)

@router.get("/db-check")
async def read_data(db: Session = Depends(db_instance.get_db)):
    try:
        db.execute("SELECT 1")
        return {
            "status": "connected",
            "message": "데이터베이스 연결에 성공했습니다!"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

