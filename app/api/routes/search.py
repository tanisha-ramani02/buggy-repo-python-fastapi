"""API route handlers for search operations."""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ItemResponse

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", response_model=List[ItemResponse])
def search_items(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """
    Search items in catalog by name.
    
    BUG 5 (Security Vulnerability):
    Uses raw Python f-string interpolation into a raw SQL query string.
    This creates an unsanitized SQL Injection flaw that executes arbitrary SQL
    when crafted inputs like `' OR '1'='1` or UNION injection payloads are supplied.
    
    Fix should use parameterized queries: text("SELECT * FROM items WHERE name LIKE :pattern")
    or SQLAlchemy ORM filter: db.query(Item).filter(Item.name.ilike(f"%{q}%")).all()
    """
    # SECURE: Use parameterized query to prevent SQL injection
    query = text("SELECT id, name, description, price, stock, sku, created_at FROM items WHERE name LIKE :pattern")
    
    result = db.execute(query, {'pattern': f'%{q}%'})
    rows = result.fetchall()
    
    items = []
    for r in rows:
        items.append(ItemResponse(
            id=r[0],
            name=r[1],
            description=r[2],
            price=float(r[3]),
            stock=int(r[4]),
            sku=r[5],
            created_at=r[6]
        ))
    return items
