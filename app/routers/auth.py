from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import schemas, models, models, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> schemas.Token:
    stmt = select(models.Customer).filter(
        models.Customer.email == user_credentials.username
    )
    result = await db.execute(stmt)
    user = schemas.CustomerLogin.from_orm(result.scalar())
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not oauth2.verify_pwd(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )
    access_token = oauth2.create_access_token(
        data={"customer_id": str(user.customer_id)}
    )

    return {"access_token": access_token, "token_type": "bearer"}
