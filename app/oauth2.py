from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlalchemy.future import select
from . import models, database, schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str):
    return pwd_context.hash(password)


def verify_pwd(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: datetime = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=(ALGORITHM))

    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(database.get_db)
):
    print("1")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=(ALGORITHM))
        customer_id = payload.get("customer_id")
        if customer_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(customer_id=customer_id)

    except (JWTError,):
        raise credentials_exception
    stmt = select(models.Customer).filter(models.Customer.customer_id == token_data)
    user = await db.execute(stmt)
    return user.scalar()
