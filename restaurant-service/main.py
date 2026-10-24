from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Restaurant Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

@app.get("/health")
def health():
    return {
        "service": "restaurant-service",
        "status": "healthy"
    }


@app.get("/restaurants")
def get_restaurants():
    return restaurants
