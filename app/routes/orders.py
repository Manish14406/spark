from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.order import Order
from app.models.product import Product

router = APIRouter()

@router.post("/orders")
def create_order(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    """
    Creates an order and reduces stock atomically.
    """

    try:
        # 1. Fetch product
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # 2. Validate stock
        if product.stock < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        # 3. Calculate total
        total_price = product.price * quantity

        # 4. Create order
        order = Order(
            product_id=product_id,
            quantity=quantity,
            total=total_price
        )
        db.add(order)

        # 5. Reduce stock
        product.stock -= quantity

        # 6. Commit both together
        db.commit()

        db.refresh(order)
        return order

    except:
        db.rollback()
        raise