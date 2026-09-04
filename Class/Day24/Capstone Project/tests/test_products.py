# tests/test_products.py

"""

Tests for product endpoints.

"""

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from app.main import app

from app.database import Base, get_db

from app.models import Product

# Test database

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():

    """Override database dependency for testing."""

    try:

        db = TestingSessionLocal()

        yield db

    finally:

        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)

def setup_database():

    """Setup test database."""

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture

def sample_product():

    """Create a sample product for testing."""

    return {

        "name": "Test Product",

        "sku": "TEST001",

        "price": 99.99,

        "stock": 10,

        "category": "Electronics",

        "description": "Test description"

    }


def test_create_product(sample_product):

    """Test creating a product."""

    response = client.post("/products", json=sample_product)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == sample_product["name"]

    assert data["sku"] == sample_product["sku"]

    assert data["price"] == sample_product["price"]

    assert data["id"] is not None


def test_create_duplicate_product(sample_product):

    """Test creating a product with duplicate SKU."""

    client.post("/products", json=sample_product)

    response = client.post("/products", json=sample_product)

    assert response.status_code == 409


def test_get_products(sample_product):

    """Test getting products list."""

    client.post("/products", json=sample_product)

    

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 1

    assert len(data["items"]) >= 1


def test_get_product_by_id(sample_product):

    """Test getting a product by ID."""

    create_response = client.post("/products", json=sample_product)

    product_id = create_response.json()["id"]

    

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id

    assert data["name"] == sample_product["name"]


def test_get_product_not_found():

    """Test getting a non-existent product."""

    response = client.get("/products/99999")

    assert response.status_code == 404


def test_update_product(sample_product):

    """Test updating a product."""

    create_response = client.post("/products", json=sample_product)

    product_id = create_response.json()["id"]

    

    update_data = {"name": "Updated Product", "price": 149.99}

    response = client.patch(f"/products/{product_id}", json=update_data)

    

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Product"

    assert data["price"] == 149.99


def test_delete_product(sample_product):

    """Test deleting a product."""

    create_response = client.post("/products", json=sample_product)

    product_id = create_response.json()["id"]

    

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 204

    

    # Verify product is deleted

    get_response = client.get(f"/products/{product_id}")

    assert get_response.status_code == 404


def test_get_categories(sample_product):

    """Test getting categories."""

    client.post("/products", json=sample_product)

    

    response = client.get("/products/categories")

    assert response.status_code == 200

    data = response.json()

    assert "Electronics" in data


def test_products_pagination(sample_product):

    """Test product pagination."""

    # Create multiple products

    for i in range(15):

        product = sample_product.copy()

        product["sku"] = f"TEST{i:03d}"

        product["name"] = f"Test Product {i}"

        client.post("/products", json=product)

    

    # Test first page

    response = client.get("/products?page=1&page_size=10")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 10

    assert data["total"] >= 15

    assert data["pages"] >= 2


def test_product_filtering(sample_product):

    """Test product filtering."""

    client.post("/products", json=sample_product)

    

    # Filter by category

    response = client.get("/products?category=Electronics")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) >= 1

    

    # Filter by search

    response = client.get("/products?search=Test")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) >= 1

