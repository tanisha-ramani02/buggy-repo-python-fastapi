"""Tests for inventory report generation and resource management."""
import os
import tempfile
from app.services.reports import export_inventory_csv, is_file_handle_closed


def test_report_generation_endpoint_success(client, sample_items):
    """Verify report generation endpoint returns 200 and valid filename."""
    res = client.post("/reports/inventory")
    assert res.status_code == 200
    data = res.json()
    assert data["record_count"] == 25
    assert os.path.exists(data["filename"])


def test_export_csv_row_count(db_session, sample_items):
    """Verify CSV export function writes header + all rows."""
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "test_inventory_rows.csv")
    
    count = export_inventory_csv(db_session, file_path)
    assert count == 25
    assert os.path.exists(file_path)


def test_empty_catalog_export(db_session):
    """Verify export works cleanly on empty catalog."""
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "test_empty_export.csv")
    
    count = export_inventory_csv(db_session, file_path)
    assert count == 0


def test_report_file_handle_not_leaked(db_session, sample_items):
    """
    BUG 6 Target Test (Resource / Connection / File Descriptor Leak):
    After exporting inventory, the underlying file handle MUST be closed
    (e.g., using `with open(...)` or explicit `f.close()`).
    Currently fails because export_inventory_csv opens the file handle
    without closing it, preventing file operations and leaking OS resources.
    """
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "test_handle_leak.csv")
    
    export_inventory_csv(db_session, file_path)
    
    # Check if the file handle was properly closed
    is_closed = is_file_handle_closed(file_path)
    assert is_closed is True, (
        f"Resource leak detected! File handle for '{file_path}' remained open after export_inventory_csv()."
    )
