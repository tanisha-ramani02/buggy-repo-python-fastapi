"""Pytest fixtures and test database setup."""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Item
from app.services.notifications import clear_dispatch_log
from app.services.reports import clear_active_handles

# Use an in-memory SQLite database with StaticPool for test isolation
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh schema before each test and tear down after."""
    Base.metadata.create_all(bind=engine)
    clear_dispatch_log()
    clear_active_handles()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Yield a database session for test setup and assertions."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_items(db_session):
    """Populate database with a standard set of 25 catalog items."""
    items = []
    for i in range(1, 26):
        item = Item(
            name=f"Product {i:02d}",
            description=f"Description for product {i}",
            price=10.0 + (i * 2.5),
            stock=100 - i,
            sku=f"SKU-PROD-{i:03d}"
        )
        db_session.add(item)
        items.append(item)
    db_session.commit()
    return items
