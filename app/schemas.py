from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ProductBase(BaseModel):
    product_name: str
    product_price: Decimal
    product_left: int

    class Config:
        orm_mode = True


class ProductOut(ProductBase):
    product_id: UUID

    class Config:
        orm_mode = True
