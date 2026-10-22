
import importlib.util
from pathlib import Path
from fastapi.testclient import TestClient

app_path = (
    Path(__file__).resolve().parents[1]
    / "restaurant-service"
    / "main.py"
)

spec = importlib.util.spec_from_file_location(
    "restaurant_app", app_path
)
restaurant_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(restaurant_module)

client = TestClient(restaurant_module.app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Restaurant Service is running!"
    }


def test_restaurants():
    response = client.get("/restaurants")

    assert response.status_code == 200

    restaurants = response.json()
    assert len(restaurants) == 2
    assert restaurants[0]["name"] == "Spice Garden"
