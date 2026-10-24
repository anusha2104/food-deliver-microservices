
from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Order Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

orders = []


@app.get("/")
def home():
    return {"message": "Order Service is running!"}

@app.get("/health")
def health():
    return {
        "service": "order-service",
        "status": "healthy"
    }


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
    updated_orders = []

    for order in orders:
        order_copy = order.copy()

        try:
            response = httpx.get( "http://delivery-service:8002/deliveries", timeout=5.0)
            response.raise_for_status()
            deliveries = response.json()

            matching_delivery = next(
                (delivery for delivery in deliveries if delivery.get("order_id") == order["id"]), None)

            if matching_delivery:
                order_copy["delivery"] = matching_delivery
        
        except (httpx.RequestError, httpx.HTTPStatusError):
            pass

        updated_orders.append(order_copy)

    return updated_orders
