from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4
from typing import Optional

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(
    db: AsyncSession = Depends(get_db),
    limit: int = 5,
    skip: int = 0,
    serch: Optional[str] = "",
) -> list[schemas.ProductOut]:
    stmt = (
        select(models.Product)
        .filter(models.Product.product_name.contains(serch))
        .limit(limit)
        .offset(skip)
    )
    result = await db.execute(stmt)
    all_products = result.scalars().all()
    return all_products


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: schemas.ProductBase, db: AsyncSession = Depends(get_db)
) -> schemas.ProductOut:
    result = await db.execute(
        select(models.Product).filter(
            models.Product.product_name == product_data.product_name
        )
    )
    if result.scalar():
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_data.product_name} already exists",
        )

    product_post = models.Product(product_id=uuid4(), **product_data.dict())
    db.add(product_post)
    await db.commit()
    return product_post
