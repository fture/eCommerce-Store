from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
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
    smtp = (
        select(models.Product)
        .filter(models.Product.product_name.contains(serch))
        .limit(limit)
        .offset(skip)
    )
    result = await db.execute(smtp)
    all_products = result.scalars().all()
    return all_products


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: schemas.ProductBase, db: AsyncSession = Depends(get_db)
) -> schemas.ProductOut:
    smtp = select(models.Product).filter(
        models.Product.product_name == product_data.product_name
    )
    result = await db.execute(smtp)

    if result.scalar():
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_data.product_name} already exists",
        )

    product_post = models.Product(product_id=uuid4(), **product_data.dict())
    db.add(product_post)
    await db.commit()
    return product_post


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: str, db: AsyncSession = Depends(get_db)
) -> schemas.ProductOut:
    target_result = await db.get(models.Product, product_id)
    if not target_result:
        raise HTTPException(status_code=404, detail="Product not found")

    return target_result


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: str,
    product_data: schemas.ProductUpdate,
    db: AsyncSession = Depends(get_db),
) -> schemas.ProductOut:
    product = await db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(product_id: str, db: AsyncSession = Depends(get_db)):
    target_product = await db.get(models.Product, product_id)
    if not target_product:
        raise HTTPException(
            status_code=404,
            detail=f"Product_id {product_id} not found",
        )

    await db.commit()
    return {"msg": "Delete product successed"}
