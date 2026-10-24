
import asyncio

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Delivery Service")

deliveries = []

# Demo timing: advance status every 20 seconds.
DEMO_DELAY_SECONDS = 20


async def simulate_delivery(delivery_id: int):
    """Automatically advance a simulated delivery."""
    stages = ["Out for Delivery", "Delivered"]

    for stage in stages:
        await asyncio.sleep(DEMO_DELAY_SECONDS)

        for delivery in deliveries:
            if delivery["id"] == delivery_id:
                # Don't overwrite a delivery already marked Delivered.
                if delivery["status"] == "Delivered":
                    return

                delivery["status"] = stage
                break
        else:
            # The delivery no longer exists.
            return


@app.get("/")
def home():
    return {"message": "Delivery Service is running!"}

@app.get("/health")
def health():
    return {
        "service": "delivery-service",
        "status": "healthy"
    }

@app.post("/deliveries")
async def create_delivery(delivery: dict):
    delivery["id"] = len(deliveries) + 1
    delivery["status"] = "Preparing"
    deliveries.append(delivery)

    # Start the timer without delaying the order response.
    asyncio.create_task(simulate_delivery(delivery["id"]))

    return delivery


@app.get("/deliveries")
def get_deliveries():
    return deliveries


@app.patch("/deliveries/{delivery_id}/status")
def update_delivery_status(delivery_id: int, status: str):
    allowed_statuses = [
        "Preparing",
        "Out for Delivery",
        "Delivered",
    ]

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid delivery status",
        )

    for delivery in deliveries:
        if delivery["id"] == delivery_id:
            delivery["status"] = status
            return delivery

    raise HTTPException(
        status_code=404,
        detail="Delivery not found",
    )
