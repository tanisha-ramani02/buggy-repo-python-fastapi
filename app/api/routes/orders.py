"""API route handlers for Order management."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import OrderCreate, OrderResponse
from app.services.orders import process_order, serialize_order_summary
from app.services.notifications import dispatch_order_alert

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    """Create and process a new customer order."""
    if not order_in.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )

    items_data = [{"item_id": it.item_id, "quantity": it.quantity} for it in order_in.items]
    order = process_order(
        db=db,
        customer_email=order_in.customer_email,
        items_data=items_data,
        discount_code=order_in.discount_code
    )

    # Trigger background alert
    await dispatch_order_alert(
        email=order.customer_email,
        order_id=order.id,
        total=order.total_amount
    )

    summary_dict = serialize_order_summary(order)
    return summary_dict
