from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProductBase(BaseModel):
    product_name: str
    product_price: Decimal
    product_left: int


class ProductUpdate(BaseModel):
    product_name: Optional[str]
    product_price: Optional[Decimal]
    product_left: Optional[int]

    class Config:
        orm_mode = True


class ProductOut(ProductBase):
    product_id: UUID

    class Config:
        orm_mode = True


class Customer(BaseModel):
    customer_first_name: str
    customer_last_name: str
    created_at: datetime

    class Config:
        orm_mode = True


class CustomerCreate(BaseModel):
    customer_first_name: str
    customer_last_name: str
    password: str
    email: str
    phone_number: Optional[str]


class CustomerUpdate(BaseModel):
    customer_first_name: Optional[str]
    customer_last_name: Optional[str]
    password: Optional[str]
    phonenum: Optional[str]
    bag_id: Optional[UUID]
    order_id: Optional[UUID]


class TokenData(BaseModel):
    id: Optional[UUID] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class CustomerLogin(BaseModel):
    password: Optional[str]
    email: Optional[str]
    customer_id: Optional[UUID]

    class Config:
        orm_mode = True
