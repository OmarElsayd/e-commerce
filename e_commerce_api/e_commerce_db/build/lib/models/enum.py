from enum import Enum


class OrderStatus(Enum):
    Placed = "Placed"
    Pending = "Pending"
    Shipped = "Shipped"
    Canceled = "Canceled"
    Delivered = "Delivered"


class PaymentStatus(Enum):
    Approved = "Approved"
    Denied = "Denied"


class Rating(Enum):
    OneStar = "OneStar"
    TwoStar = "TwoStar"
    ThreeStar = "ThreeStar"
    FourStar = "FourStar"
    FiveStar = "FiveStar"


class Role(Enum):
    Admin = "Admin"
    User = "User"

