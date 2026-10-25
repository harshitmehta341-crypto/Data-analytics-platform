
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
    # Use a separate in-memory database for each test.
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def create_sample_record(client):
    return client.post(
        "/api/v1/records",
        json={
            "product": "Laptop",
            "category": "Electronics",
            "quantity": 2,
            "unit_price": 50000,
        },
    )


def test_health_check(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_record(client):
    response = create_sample_record(client)

    assert response.status_code == 201
    assert response.json()["product"] == "Laptop"
    assert response.json()["total_value"] == 100000


def test_read_record(client):
    created = create_sample_record(client)
    record_id = created.json()["id"]

    response = client.get(f"/api/v1/records/{record_id}")

    assert response.status_code == 200
    assert response.json()["id"] == record_id
    assert response.json()["quantity"] == 2


def test_update_record(client):
    created = create_sample_record(client)
    record_id = created.json()["id"]

    response = client.put(
        f"/api/v1/records/{record_id}",
        json={
            "product": "Laptop",
            "category": "Electronics",
            "quantity": 3,
            "unit_price": 50000,
        },
    )

    assert response.status_code == 200
    assert response.json()["total_value"] == 150000


def test_delete_record(client):
    created = create_sample_record(client)
    record_id = created.json()["id"]

    response = client.delete(f"/api/v1/records/{record_id}")

    assert response.status_code == 200

    missing = client.get(f"/api/v1/records/{record_id}")
    assert missing.status_code == 404


def test_invalid_quantity_is_rejected(client):
    response = client.post(
        "/api/v1/records",
        json={
            "product": "Laptop",
            "category": "Electronics",
            "quantity": -1,
            "unit_price": 50000,
        },
    )

    assert response.status_code == 422


def test_analytics_summary(client):
    create_sample_record(client)

    response = client.get("/api/v1/analytics/summary")

    assert response.status_code == 200

    data = response.json()
    assert data["total_records"] == 1
    assert data["total_revenue"] == 100000


def test_category_analytics(client):
    create_sample_record(client)

    response = client.get("/api/v1/analytics/categories")

    assert response.status_code == 200

    categories = response.json()["categories"]
    assert len(categories) == 1
    assert categories[0]["category"] == "Electronics"
    assert categories[0]["revenue"] == 100000


def test_top_products(client):
    create_sample_record(client)

    response = client.get("/api/v1/analytics/top-products")

    assert response.status_code == 200

    products = response.json()["products"]
    assert len(products) == 1
    assert products[0]["product"] == "Laptop"
    assert products[0]["revenue"] == 100000
