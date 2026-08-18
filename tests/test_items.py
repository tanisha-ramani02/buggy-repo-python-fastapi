"""Tests for Item API endpoints and input validation."""


def test_create_valid_item(client):
    """Test creating a valid item returns 201 and valid response body."""
    payload = {
        "name": "Mechanical Keyboard",
        "description": "RGB Mechanical Keyboard",
        "price": 89.99,
        "stock": 50,
        "sku": "SKU-KEY-001"
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Mechanical Keyboard"
    assert data["price"] == 89.99
    assert data["stock"] == 50
    assert data["sku"] == "SKU-KEY-001"
    assert "id" in data


def test_get_existing_item(client, sample_items):
    """Test retrieving an item by ID."""
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data


def test_create_duplicate_sku_rejected(client):
    """Test creating an item with duplicate SKU returns 400 Bad Request."""
    payload = {
        "name": "Item A",
        "price": 10.0,
        "stock": 5,
        "sku": "SKU-DUP-123"
    }
    res1 = client.post("/items/", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/items/", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]


def test_create_item_negative_price_rejected(client):
    """
    BUG 2 Target Test (Missing Input Validation):
    Attempting to create an item with negative price (-25.0) or negative stock (-5)
    should be rejected with 422 or 400 status.
    Currently fails because the endpoint does not validate price > 0 or stock >= 0.
    """
    payload = {
        "name": "Invalid Item",
        "description": "Item with negative price",
        "price": -25.0,
        "stock": 10,
        "sku": "SKU-NEG-999"
    }
    response = client.post("/items/", json=payload)
    assert response.status_code in [400, 422], (
        f"Expected 400 or 422 for negative price, but got {response.status_code}: {response.text}"
    )
