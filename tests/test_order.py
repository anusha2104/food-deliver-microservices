import importlib.util
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient

app_path = (
    Path(__file__).resolve().parents[1]
    / "order-service"
    / "main.py"
)

import sys

spec = importlib.util.spec_from_file_location(
    "order_app", app_path
)
order_module = importlib.util.module_from_spec(spec)
sys.modules["order_app"] = order_module
spec.loader.exec_module(order_module)

client = TestClient(order_module.app)


@patch("order_app.httpx.get")
def test_invalid_restaurant(mock_get):
    mock_get.return_value.json.return_value = [
        {"id": 1, "name": "Spice Garden"}
    ]
    mock_get.return_value.raise_for_status.return_value = None

    response = client.post(
        "/orders",
        json={
            "restaurant_id": 999,
            "customer": "Test",
            "item": "Pizza"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Restaurant not found"


@patch("order_app.httpx.post")
@patch("order_app.httpx.get")
def test_valid_restaurant(mock_get, mock_post):
    mock_get.return_value.json.return_value = [
        {"id": 1, "name": "Spice Garden"}
    ]
    mock_get.return_value.raise_for_status.return_value = None

    mock_post.return_value.json.return_value = {
        "order_id": 1,
        "restaurant_id": 1,
        "id": 1,
        "status": "Preparing"
    }
    mock_post.return_value.raise_for_status.return_value = None

    response = client.post(
        "/orders",
        json={
            "restaurant_id": 1,
            "customer": "Test",
            "item": "Pizza"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Placed"
    assert response.json()["delivery"]["status"] == "Preparing"