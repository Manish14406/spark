from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import get_db
from app.models.creator import Creator
from app.utils.security import hash_password

router = APIRouter()

class CreatorCreate(BaseModel):
    name: str
    email: str
    password: str

@router.post("/creators")
def create_creator(data: CreatorCreate, db: Session = Depends(get_db)):
    """
    Register new creator with hashed password.
    """

    existing = db.query(Creator).filter(Creator.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_creator = Creator(
        name=data.name,
        email=data.email,
        password=hash_password(data.password)
    )

    db.add(new_creator)
    db.commit()
    db.refresh(new_creator)

    return {"id": new_creator.id, "email": new_creator.email}