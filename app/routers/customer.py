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


@router.get("/{customer_id}", status_code=status.HTTP_200_OK)
async def get_user(customer_id: str, db: AsyncSession = Depends(get_db)):
    try:
        stmp = select(models.Customer).filter(models.Customer.email == customer_id)
        user = await db.execute(stmp)
        return user.scalar()
    except:
        raise HTTPException(status_code=404, detail={"msg": "Customer does not exist"})


@router.put("/{email}", status_code=status.HTTP_200_OK)
async def update_user(
    email: str,
    customer_data: schemas.CustomerUpdate,
    db: AsyncSession = Depends(get_db),
):
    stmp = select(models.Customer).filter(models.Customer.email == email)
    user = await db.execute(stmp)
    user_data = user.scalar()
    for key, value in customer_data.dict(exclude_unset=True).items():
        setattr(user_data, key, value)
    db.add(user_data)
    await db.commit()
    return user_data


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(customer_id: str, db: AsyncSession = Depends(get_db)):
    try:
        target_customer = await db.get(models.Customer, customer_id)
        if not target_customer:
            raise HTTPException(
                status_code=404,
                detail=f"customer not found",
            )
    except:
        raise HTTPException(
            status_code=404,
            detail=f"customer {customer_id} is not found",
        )
    await db.delete(target_customer)
    await db.commit()
    return {"msg": "Delete customer successed !"}
