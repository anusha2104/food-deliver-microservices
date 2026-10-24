from sqlalchemy import Column, Integer, String, Float
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(String, nullable=False)
    customer = Column(String, nullable=False)
    item = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, default="Placed", nullable=False)

    