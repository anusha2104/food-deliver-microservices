
from fastapi import FastAPI

app = FastAPI(title="Restaurant Service")

restaurants = [
    {
        "id": 1,
        "name": "Spice Garden",
        "cuisine": "Indian",
        "available": True
    },
    {
        "id": 2,
        "name": "Pizza Corner",
        "cuisine": "Italian",
        "available": True
    }
]


@app.get("/")
def home():
    return {"message": "Restaurant Service is running!"}


@app.get("/restaurants")
def get_restaurants():
    return restaurants
