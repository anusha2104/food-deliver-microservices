
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="Order Service")

orders = []


@app.get("/")
def home():
    return {"message": "Order Service is running!"}


@app.post("/orders")
def create_order(order: dict):
    restaurant_id = order.get("restaurant_id")

    try:
        response = httpx.get(
            "http://restaurant-service:8000/restaurants",
            timeout=5.0
        )
        response.raise_for_status()
        restaurants = response.json()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail="Restaurant Service is unavailable"
        )

    restaurant_exists = any(
        restaurant["id"] == restaurant_id
        for restaurant in restaurants
    )

    if not restaurant_exists:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    order["id"] = len(orders) + 1
    order["status"] = "Placed"
    orders.append(order)
    
    try:
        response = httpx.post(
            "http://delivery-service:8002/deliveries",
            json={
                "order_id": order["id"],
                "restaurant_id": restaurant_id
            }, timeout=5.0)
        response.raise_for_status()
        order["delivery"] = response.json()

    except httpx.HTTPError:
        order["delivery"] = {"status": "Could not contact Delivery Service"}
    return order


@app.get("/orders")
def get_orders():
    return orders
