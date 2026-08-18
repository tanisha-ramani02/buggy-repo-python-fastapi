"""Tests for Order processing and response data transformation."""
from app.services.orders import process_order, serialize_order_summary
from app.models import Item


def test_order_processing_db_commit(db_session, sample_items):
    """Verify order records and line items are properly saved in DB."""
    order = process_order(
        db=db_session,
        customer_email="alice@example.com",
        items_data=[{"item_id": 1, "quantity": 2}, {"item_id": 2, "quantity": 1}]
    )
    assert order.id is not None
    assert order.customer_email == "alice@example.com"
    assert len(order.items) == 2


def test_order_discount_code_applied(db_session, sample_items):
    """Verify 10% coupon discount is applied when SAVE10 code is used."""
    order = process_order(
        db=db_session,
        customer_email="bob@example.com",
        items_data=[{"item_id": 1, "quantity": 2}],  # 2 * 12.50 = 25.00 -> 10% off = 22.50 + 8% tax = 24.30
        discount_code="SAVE10"
    )
    assert order.discount_code == "SAVE10"
    assert order.total_amount < 27.00


def test_order_empty_items_rejected(client):
    """Verify attempting to create an order with empty items returns 400."""
    res = client.post("/orders/", json={"customer_email": "test@example.com", "items": []})
    assert res.status_code == 400


def test_order_serializer_includes_tax_amount(db_session, sample_items):
    """
    BUG 4 Target Test (Data Transformation Bug):
    The API serializer serialize_order_summary MUST include 'tax_amount'
    in the transformed dictionary response according to API contracts.
    Currently fails because serialize_order_summary omits 'tax_amount'.
    """
    order = process_order(
        db=db_session,
        customer_email="charlie@example.com",
        items_data=[{"item_id": 1, "quantity": 2}]
    )
    summary = serialize_order_summary(order)
    
    assert "tax_amount" in summary, (
        f"API contract violation: 'tax_amount' missing from serialized order dictionary: {summary}"
    )
    assert summary["tax_amount"] == order.tax_amount
    assert summary["tax_amount"] > 0
