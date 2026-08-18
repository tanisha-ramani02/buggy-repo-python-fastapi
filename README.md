# Inventory & Orders Management API (Testbed Codebase)

A lightweight Python FastAPI + SQLite backend service engineered as the target testbed for the **Autonomous Bug Fixer Agent**.

## System Architecture & Components
- **Framework**: FastAPI (async ASGI framework)
- **Database**: SQLite (SQLAlchemy ORM + SessionLocal)
- **Validation & Serialization**: Pydantic v2
- **Testing**: Pytest & Pytest-Asyncio (24 comprehensive test cases)

---

## Directory Structure
```text
buggy-repo-python-fastapi/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── items.py        # Item CRUD & stock management
│   │       ├── orders.py       # Order checkout & serialization
│   │       ├── reports.py      # Inventory export endpoints
│   │       └── search.py       # Catalog search & filter
│   ├── services/
│   │   ├── catalog.py          # Pagination & pricing calculation
│   │   ├── notifications.py    # Async alert dispatcher
│   │   ├── orders.py           # Order processing & response transformation
│   │   └── reports.py          # CSV export & file streaming
│   ├── database.py             # SQLite engine & session dependency
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   └── main.py                 # FastAPI application factory
├── tests/
│   ├── conftest.py             # In-memory SQLite fixtures & TestClient
│   ├── test_async.py           # Async dispatch tests
│   ├── test_catalog.py         # Pagination & discount tests
│   ├── test_items.py           # Item creation & validation tests
│   ├── test_orders.py          # Order transformation tests
│   ├── test_reports.py         # Report generation & resource tests
│   └── test_security.py        # Search & SQL injection tests
├── pyproject.toml              # Dependencies & pytest configuration
└── README.md
```

---

## Running the Test Suite
```bash
# Setup virtual environment and sync dependencies
uv sync

# Run the full test suite (18 passed, 6 failed initially)
uv run pytest -v
```

---

## Target Test Failures Overview
The repository contains 24 pytest test cases, with exactly 6 initial failing tests corresponding to the 6 evaluation categories. See `FAILED_TESTS_CATALOG.md` for details.