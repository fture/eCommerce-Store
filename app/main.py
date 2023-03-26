from fastapi import FastAPI
from .routers import customer, product, auth, order

app = FastAPI()

# app.include_router(customer.router, prefix="/user", tags=["customers"])
app.include_router(product.router, prefix="/product", tags=["products"])
# app.include_router(order.router, tags=["orders"])
# app.include_router(auth.router, tags=["Authentication"])


@app.get("/")
async def root():
    return {"msg": "Hello, world!"}
