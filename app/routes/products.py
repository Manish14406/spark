from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user

from app.db.database import get_db
from app.models.product import Product
from app.models.creator import Creator


router = APIRouter()

@router.post("/products")
def create_product(
    creator_id: int,
    name: str,
    price: float,
    stock: int = 0,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)   # JWT PROTECTION
):
    """
    Creates a product for a creator.
    """

    # 1. Make sure creator exists
    creator = db.query(Creator).filter(Creator.id == creator_id).first()
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")

    # 2. Create product
    product = Product(
        creator_id=creator_id,
        name=name,
        price=price,
        stock=stock
    )

    # 3. Save to DB
    db.add(product)
    db.commit()
    db.refresh(product)

    return product