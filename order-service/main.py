from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import httpx
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from database import Base, engine, SessionLocal
from models import Order

app = FastAPI(title="Order Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("DATABASE_URL"):
    Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Order Service is running!"}


@app.get("/health")
def health():
    try:
        with engine.connect():
            pass
        return {"service": "order-service", "status": "healthy"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")


@app.post("/orders")
def create_order(order: dict):
    restaurant_id = order.get("restaurant_id")

    try:
        response = httpx.get(
            "http://restaurant-service:8000/restaurants",
            timeout=5.0,
        )
        response.raise_for_status()
        restaurants = response.json()
    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail="Restaurant Service is unavailable",
        )

    if not any(r["id"] == restaurant_id for r in restaurants):
        raise HTTPException(status_code=404, detail="Restaurant not found")

    db: Session = SessionLocal()
    try:
        new_order = Order(
            restaurant_id=restaurant_id,
            customer=order.get("customer", "Guest"),
            item=order.get("item", ""),
            price=order.get("price", 0),
            status="Placed",
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        result = {
            "id": new_order.id,
            "restaurant_id": new_order.restaurant_id,
            "customer": new_order.customer,
            "item": new_order.item,
            "price": new_order.price,
            "status": new_order.status,
        }

        try:
            response = httpx.post(
                "http://delivery-service:8002/deliveries",
                json={
                    "order_id": new_order.id,
                    "restaurant_id": restaurant_id,
                },
                timeout=5.0,
            )
            response.raise_for_status()
            result["delivery"] = response.json()
        except httpx.HTTPError:
            result["delivery"] = {
                "status": "Could not contact Delivery Service"
            }

        return result
    finally:
        db.close()


@app.get("/orders")
def get_orders():
    db: Session = SessionLocal()
    try:
        orders = db.query(Order).order_by(Order.id).all()
        updated_orders = []

        try:
            response = httpx.get(
                "http://delivery-service:8002/deliveries",
                timeout=5.0,
            )
            response.raise_for_status()
            deliveries = response.json()
        except httpx.HTTPError:
            deliveries = []

        for order in orders:
            result = {
                "id": order.id,
                "restaurant_id": order.restaurant_id,
                "customer": order.customer,
                "item": order.item,
                "price": order.price,
                "status": order.status,
            }

            matching = next(
                (
                    d for d in deliveries
                    if d.get("order_id") == order.id
                ),
                None,
            )
            if matching:
                result["delivery"] = matching

            updated_orders.append(result)

        return updated_orders
    finally:
        db.close()