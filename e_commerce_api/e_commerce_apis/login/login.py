import logging

from e_commerce_api.e_commerce_apis.dependency.jwt_auth import verify_password, JwtAuth
from e_commerce_api.e_commerce_apis.dependency.role_checker import user_pass
from e_commerce_api.e_commerce_apis.dependency.users import get_curr_user
from e_commerce_api.e_commerce_apis.util.set_session import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from e_commerce_api.e_commerce_db.models.models import Users
from jose.jwt import JWTError

from e_commerce_api.e_commerce_db.models.enum import Role

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("login api")


router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={
        404: {"description": "Not found"}
    }
)

jwt_auth = JwtAuth()


class TokenResponse(BaseModel):
    status_code: int
    access_token: str
    token_type: str = "bearer"


@router.post(
    "",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(creds_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    username = creds_form.username
    user = session.query(Users).filter(Users.user_name == username).first()

    if not user or not verify_password(creds_form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    token_payload = {
        "id": user.id,
        "user_name": user.user_name,
    }
    try:
        token = jwt_auth.create_access_token(token_payload)

        return TokenResponse(
            status_code=status.HTTP_200_OK,
            access_token=token,
        )

    except JWTError as jwt_error:
        logger.error(jwt_error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(jwt_error)
        )


@router.get(
    "/profile"
)
async def get_info(user: Users = Depends(user_pass)):
    return {
        "profile": user
    }
