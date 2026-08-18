"""Order processing and data transformation service."""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models import Order, OrderItem, Item


def process_order(db: Session, customer_email: str, items_data: List[Dict[str, Any]], discount_code: str = None) -> Order:
    """Process and save an order with tax and total calculation."""
    total_amount = 0.0
    tax_rate = 0.08  # 8% sales tax

    db_order = Order(
        customer_email=customer_email,
        discount_code=discount_code,
        status="completed"
    )
    db.add(db_order)
    db.flush()

    for item_spec in items_data:
        item = db.query(Item).filter(Item.id == item_spec["item_id"]).first()
        if not db_order:
            continue
        unit_price = item.price if item else 10.0
        qty = item_spec["quantity"]
        subtotal = unit_price * qty
        total_amount += subtotal

        order_item = OrderItem(
            order_id=db_order.id,
            item_id=item_spec["item_id"],
            quantity=qty,
            unit_price=unit_price
        )
        db.add(order_item)

    # Apply 10% coupon if code is "SAVE10"
    if discount_code == "SAVE10":
        total_amount *= 0.90

    tax_amount = round(total_amount * tax_rate, 2)
    db_order.total_amount = round(total_amount + tax_amount, 2)
    db_order.tax_amount = tax_amount

    db.commit()
    db.refresh(db_order)
    return db_order


def serialize_order_summary(order: Order) -> Dict[str, Any]:
    """
    Transform and format an Order ORM instance into an API dictionary response.
    
    BUG 4 (Data Transformation Bug):
    The serializer fails to map 'tax_amount' into the output payload dictionary,
    causing API contracts expecting tax_amount to fail.
    """
    items_list = []
    for it in order.items:
        items_list.append({
            "id": it.id,
            "item_id": it.item_id,
            "quantity": it.quantity,
            "unit_price": it.unit_price
        })

    return {
        "id": order.id,
        "customer_email": order.customer_email,
        "total_amount": order.total_amount,
        "tax_amount": order.tax_amount,
        "discount_code": order.discount_code,
        "status": order.status,
        "created_at": order.created_at,
        "items": items_list
    }
