from fastapi import FastAPI
from typing import List
from pydantic import BaseModel, Field
from enum import Enum


class StatusEnum(str, Enum):
    pending = 'pending'
    completed = 'completed'
    canceled = 'canceled'


class Order(BaseModel):
    id: int
    item: str
    quantity: int = Field(ge=0, description="The price must be positive number")
    price: float = Field(ge=0, description="The price must be positive number")
    status: StatusEnum


class Query(BaseModel):
    orders: List[Order] = []
    criterion: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/solution")
def process_orders(query: Query):
    orders = query.orders
    criterion = query.criterion
    total_revenue: float = 0
    for order in orders:
        if criterion == "all" or criterion == order.status:
            total_revenue += order.price * order.quantity
    return total_revenue
