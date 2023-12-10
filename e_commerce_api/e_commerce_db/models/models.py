import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Unicode,
    Float,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship
from .base import Base
from .enum import OrderStatus, Rating, PaymentStatus, Role


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(Text, nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)
    phone_number = Column(Unicode(12), nullable=False)
    role = Column(Enum(Role), nullable=False)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    quantity_available = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=True)
    image_url = Column(Text, nullable=False)

    category = relationship(Category)


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.utcnow())
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    conformation_number = Column(String(30), nullable=False)

    users = relationship(Users)


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey(Orders.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Products.id), nullable=False)
    quantity = Column(Integer, nullable=True)
    price = Column(Float, nullable=False)

    orders = relationship(Orders)
    products = relationship(Products)


class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Products.id), nullable=False)
    rating = Column(Enum(Rating), default=Rating.FiveStar.value)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())

    users = relationship(Users)
    product = relationship(Products)


class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey(Orders.id), nullable=False)
    payment_date = Column(DateTime, default=datetime.datetime.utcnow())
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)

    orders = relationship(Orders)






