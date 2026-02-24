from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import get_db
from app.models.lead import Lead
from app.models.creator import Creator
from app.utils.auth import get_current_user

router = APIRouter()


# ========= Pydantic Schema =========

class LeadCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None
    source: str | None = None


# ========= CREATE LEAD =========

@router.post("/leads")
def create_lead(
    data: LeadCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Creates a new lead for the logged-in creator.
    """

    # 1. Make sure creator exists (safety check)
    creator = db.query(Creator).filter(Creator.id == user_id).first()
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")

    # 2. Prevent duplicate email per creator
    existing_lead = (
        db.query(Lead)
        .filter(Lead.creator_id == user_id, Lead.email == data.email)
        .first()
    )

    if existing_lead:
        raise HTTPException(status_code=400, detail="Lead already exists for this creator")

    # 3. Create lead
    new_lead = Lead(
        creator_id=user_id,
        name=data.name,
        email=data.email,
        phone=data.phone,
        source=data.source
    )

    # 4. Save to DB
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return new_lead


# ========= GET LEADS =========

@router.get("/leads")
def get_leads(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(Lead).filter(Lead.creator_id == user_id).all()