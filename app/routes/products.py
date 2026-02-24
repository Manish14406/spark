from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user

from app.db.database import get_db
from app.models.product import Product
from app.models.creator import Creator


router = APIRouter()

from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

@router.post("/products")
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    product = Product(
        creator_id=user_id,
        name=data.name,
        price=data.price,
        stock=data.stock
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

@router.get("/products")
def get_products(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(Product).filter(Product.creator_id == user_id).all()