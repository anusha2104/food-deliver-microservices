from fastapi import FastAPI

app = FastAPI(title="Delivery Service")

deliveries = []

@app.get("/")
def home():
    return {"message": "Delivery Service is running!"}

@app.post("/deliveries")
def create_delivery(delivery: dict):
    delivery["id"] = len(deliveries) + 1
    delivery["status"] = "Preparing"
    deliveries.append(delivery)

    return delivery

@app.get("/deliveries")
def get_deliveries():
    return deliveries