from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.lead import Lead
from app.models.creator import Creator

router = APIRouter()

@router.post("/leads")
def create_lead(
    creator_id: int,
    name: str,
    email: str,
    phone: str = None,
    source: str = None,
    db: Session = Depends(get_db)
):
    """
    Creates a new lead for a specific creator.
    """

    # 1. Make sure creator exists
    creator = db.query(Creator).filter(Creator.id == creator_id).first()
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    
    # 2. Check if this email already exists for this creator
    existing_lead = (
        db.query(Lead)
        .filter(Lead.creator_id == creator_id, Lead.email == email)
        .first()
    )

    if existing_lead:
        raise HTTPException(status_code=400, detail="Lead already exists for this creator")
    # 3. Create lead object
    new_lead = Lead(
        creator_id=creator_id,
        name=name,
        email=email,
        phone=phone,
        source=source
    )
    
    # 4. Save to DB
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return new_lead

