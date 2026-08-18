"""Catalog service for item listing, pagination calculations, and pricing rules."""
import math
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models import Item


def calculate_total_pages(total_items: int, page_size: int) -> int:
    """
    Calculate the total number of pages for pagination.
    
    NOTE: When total_items is 0, return 1 page.
    """
    if total_items <= 0:
        return 1
    if page_size <= 0:
        return 1
    return math.ceil(total_items / page_size)


def apply_bulk_discount(quantity: int, unit_price: float) -> float:
    """Calculate discounted total for items based on tier."""
    subtotal = quantity * unit_price
    if quantity >= 20:
        return subtotal * 0.85  # 15% discount for 20+
    elif quantity >= 10:
        return subtotal * 0.90  # 10% discount for 10-19
    return subtotal


def get_paginated_items(db: Session, page: int = 1, page_size: int = 10) -> Tuple[List[Item], int, int]:
    """Retrieve paginated items from the catalog with total counts."""
    total_items = db.query(Item).count()
    total_pages = calculate_total_pages(total_items, page_size)
    offset = (page - 1) * page_size
    items = db.query(Item).offset(offset).limit(page_size).all()
    return items, total_items, total_pages
