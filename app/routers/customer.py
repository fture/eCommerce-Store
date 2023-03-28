from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, schemas
from ..database import get_db

router = APIRouter()


# PUBLIC METHODS
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(db: AsyncSession = Depends(get_db)) -> list[schemas.Customer]:
    stmp = select(models.Customer)
    all_user = await db.execute(stmp)
    return all_user.scalars().all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: schemas.CustomerCreate, db: AsyncSession = Depends(get_db)
) -> schemas.Customer:
    stmp = select(models.Customer).filter(models.Customer.email == user_data.email)
    user = await db.execute(stmp)
    if user.scalar():
        raise HTTPException(status_code=404, detail={"msg": "Customer already exist"})
    post_user = models.Customer(
        customer_id=uuid4(), **user_data.dict(exclude_unset=True)
    )
    db.add(post_user)
    await db.commit()
    return post_user


# PRIVATE METHODS


@router.get("/{email}", status_code=status.HTTP_200_OK)
async def get_user(email: str, db: AsyncSession = Depends(get_db)):
    stmp = select(models.Customer).filter(models.Customer.email == email)
    user = await db.execute(stmp)
    return user.scalar()


@router.put("/{email}", status_code=status.HTTP_200_OK)
async def update_user(email: str, password: str, db: AsyncSession = Depends(get_db)):
    pass
