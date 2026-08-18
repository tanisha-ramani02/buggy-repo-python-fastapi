"""API route handlers for Item Inventory operations."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Item
from app.schemas import ItemCreate, ItemUpdate, ItemResponse, PaginatedItemsResponse, PaginationMeta
from app.services.catalog import get_paginated_items

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new inventory item.
    
    BUG 2 (Missing Input Validation):
    Endpoint fails to validate that 'price' must be strictly positive (> 0)
    and 'stock' must be non-negative (>= 0).
    Negative prices or negative stock corrupt downstream accounting.
    """
    # Check if SKU already exists
    existing = db.query(Item).filter(Item.sku == item_in.sku).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item with this SKU already exists"
        )
    
    # MISSING VALIDATION:
    # No check for item_in.price <= 0 or item_in.stock < 0
    # Should raise HTTPException(status_code=422, detail="Price and stock must be positive")
    
    new_item = Item(
        name=item_in.name,
        description=item_in.description,
        price=item_in.price,
        stock=item_in.stock,
        sku=item_in.sku
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/", response_model=PaginatedItemsResponse)
def list_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieve catalog items with pagination."""
    items, total_items, total_pages = get_paginated_items(db, page=page, page_size=page_size)
    return PaginatedItemsResponse(
        items=[ItemResponse.model_validate(it) for it in items],
        pagination=PaginationMeta(
            total_items=total_items,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    )


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get single item by ID."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete item by ID."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(item)
    db.commit()
    return None
