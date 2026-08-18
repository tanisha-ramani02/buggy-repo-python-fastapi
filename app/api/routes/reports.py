"""API route handlers for inventory reports."""
import os
import tempfile
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ReportResponse
from app.services.reports import export_inventory_csv

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/inventory", response_model=ReportResponse, status_code=status.HTTP_200_OK)
def generate_inventory_report(db: Session = Depends(get_db)):
    """Generate and export a CSV report of the current inventory."""
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "inventory_export.csv")
    
    count = export_inventory_csv(db, file_path)
    return ReportResponse(
        message="Inventory report generated successfully",
        filename=file_path,
        record_count=count
    )
