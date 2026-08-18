"""Tests for search functionality and SQL Injection vulnerability."""


def test_search_valid_keyword(client, sample_items):
    """Test searching for a specific product name."""
    res = client.get("/search/?q=Product 01")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["name"] == "Product 01"


def test_search_no_matches(client, sample_items):
    """Test searching for non-existent term returns empty list."""
    res = client.get("/search/?q=NonExistentProductXYZ")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 0


def test_search_requires_query_param(client):
    """Test calling search without 'q' parameter returns 422 validation error."""
    res = client.get("/search/")
    assert res.status_code == 422


def test_search_sanitization_against_sql_injection(client, sample_items):
    """
    BUG 5 Target Test (Security Vulnerability / SQL Injection):
    A crafted SQL injection payload like `' OR '1'='1` should be treated as literal text
    and return 0 results (since no item is literally named "' OR '1'='1").
    Currently fails because raw string interpolation executes the condition '1'='1',
    leaking all 25 catalog items.
    """
    injection_payload = "' OR '1'='1"
    res = client.get(f"/search/?q={injection_payload}")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 0, (
        f"SQL Injection flaw detected! Expected 0 results for literal search payload '{injection_payload}', "
        f"but received {len(data)} items due to un-sanitized raw SQL interpolation."
    )
