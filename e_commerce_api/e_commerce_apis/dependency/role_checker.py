import logging

from fastapi import Depends, HTTPException, status
from e_commerce_api.e_commerce_apis.dependency.users import get_curr_user
from e_commerce_api.e_commerce_db.models.enum import Role
from e_commerce_api.e_commerce_db.models.models import Users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("products api")


class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Users = Depends(get_curr_user)):
        if user.role not in self.allowed_roles:
            logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
        return user


admin_pass = RoleChecker([Role.Admin])
user_pass = RoleChecker([Role.User, Role.Admin])
seller_pass = RoleChecker([Role.Seller, Role.Admin])
