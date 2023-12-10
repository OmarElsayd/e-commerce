from fastapi import FastAPI

from .products import products
from .register import register
from .login import login
from .orders import order


app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(order.router)
app.include_router(products.router)
