"""Pydantic schemas for request validation and response serialization."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    sku: str


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


class ItemResponse(ItemBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_email: str
    items: List[OrderItemCreate]
    discount_code: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    customer_email: str
    total_amount: float
    tax_amount: float
    discount_code: Optional[str] = None
    status: str
    created_at: datetime
    items: List[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


class PaginationMeta(BaseModel):
    total_items: int
    page: int
    page_size: int
    total_pages: int


class PaginatedItemsResponse(BaseModel):
    items: List[ItemResponse]
    pagination: PaginationMeta


class ReportResponse(BaseModel):
    message: str
    filename: str
    record_count: int
