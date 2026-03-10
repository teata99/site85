import os
from datetime import datetime
from fastapi import APIRouter, Depends
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env02"
load_dotenv(dotenv_path=env_path)

router = APIRouter()

class Database:
    def __init__(self):
        self.db_url = os.getenv("POSTGRES_URL_NON_POOLING")

        if self.db_url and self.db_url.startswith("postgres://"):
            self.db_url = self.db_url.replace("postgres://", "postgresql://", 1)

        if not self.db_url:
            raise ValueError("POSTGRES_URL_NON_POOLING 환경 변수가 설정되지 않았습니다.")
        
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

class Memo(db_instance.Base):
    __tablename__ = "memos"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)

db_instance.Base.metadata.create_all(bind=db_instance.engine)    

class MemoCreate(BaseModel):
    content: str

@router.post("/memos")
async def create_memo(memo: MemoCreate, db: Session = Depends(db_instance.get_db)):
    new_memo = Memo(content=memo.content)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)
    return {"message": "메모 저장 성공!", "id": new_memo.id}

@router.get("/memos")
async def get_memos(db: Session = Depends(db_instance.get_db)):
    memos = db.query(Memo).order_by(Memo.id.desc()).all()
    return memos

@router.get("/db-check")
async def read_data(db: Session = Depends(db_instance.get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "connected",
            "message": "데이터베이스 연결에 성공했습니다!"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

