from dataclasses import dataclass
from typing import Tuple
from fastapi import Form
from pydantic import BaseModel

from e_commerce_api.e_commerce_db.models.enum import Role


@dataclass
class InCompingTokenPayload:
    id: int
    user_name: str


@dataclass
class TokenPayload:
    sub: str
    exp: float


class UserInput(BaseModel):
    user_name: str
    email: str
    password: str
    first_name: str
    last_name: str
    address: str
    phone_number: str


class SignupOutput(BaseModel):
    status_code: int


class OrderPayload(BaseModel):
    """
    [0] -> product_id
    [1] -> quantity
    [2] -> price
    """
    product_ids: list[Tuple[int, int, float]]


class OrderConfirmation(BaseModel):
    status_code: int
    conformation_number: str


class ProductInputForm(BaseModel):
    name: str = Form(...)
    description: str = Form(...)
    price: float = Form(...)
    category_id: int = Form(...)
    quantity_available: int = Form(...)
    image_url: str = Form(...)

