"""Reporting service for exporting inventory summary and logs."""
import os
import csv
from typing import List, Any
from sqlalchemy.orm import Session
from app.models import Item

# Registry tracking opened file handles for resource leak auditing
_ACTIVE_HANDLES: List[Any] = []


def export_inventory_csv(db: Session, file_path: str) -> int:
    """
    Export current inventory items to a CSV file.
    
    BUG 6 (Resource / Connection Leak):
    Opens a file descriptor without a context manager (`with open(...)`)
    or explicit `f.close()`, leaving the file descriptor locked and leaking OS resources.
    
    Fix: Use `with open(file_path, "w", newline="", encoding="utf-8") as f:`
    so the file is automatically and safely closed.
    """
    items = db.query(Item).all()
    
    # LEAK: File opened directly without closing or context manager
    f = open(file_path, "w", newline="", encoding="utf-8")
    _ACTIVE_HANDLES.append(f)
    writer = csv.writer(f)
    writer.writerow(["ID", "Name", "SKU", "Price", "Stock"])
    
    count = 0
    for item in items:
        writer.writerow([item.id, item.name, item.sku, item.price, item.stock])
        count += 1
    
    # Missing f.close() or with open(...) context manager
    return count


def is_file_handle_closed(file_path: str) -> bool:
    """Audit whether all handles for the given file have been closed."""
    for handle in _ACTIVE_HANDLES:
        if getattr(handle, "name", None) == file_path:
            if not handle.closed:
                return False
    return True


def clear_active_handles():
    """Clear handle registry between tests."""
    _ACTIVE_HANDLES.clear()
