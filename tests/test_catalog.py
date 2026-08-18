"""Tests for catalog pagination and discount calculations."""
from app.services.catalog import calculate_total_pages, apply_bulk_discount


def test_discount_standard_pricing():
    """Verify standard pricing without discount for quantities under 10."""
    price = apply_bulk_discount(quantity=5, unit_price=20.0)
    assert price == 100.0


def test_discount_bulk_tier():
    """Verify 15% discount for 20+ items."""
    price = apply_bulk_discount(quantity=20, unit_price=10.0)
    assert price == 170.0


def test_pagination_exact_multiple():
    """Verify total pages when total items is an exact multiple of page size."""
    pages = calculate_total_pages(total_items=20, page_size=10)
    assert pages == 2


def test_pagination_odd_items_total_pages():
    """
    BUG 1 Target Test (Off-by-one / Logic Error):
    When total_items = 25 and page_size = 10, there should be 3 total pages
    (page 1: 10 items, page 2: 10 items, page 3: 5 items).
    Currently fails because integer division 25 // 10 yields 2 instead of 3.
    """
    total_pages = calculate_total_pages(total_items=25, page_size=10)
    assert total_pages == 3, f"Expected 3 pages for 25 items with page size 10, got {total_pages}"
