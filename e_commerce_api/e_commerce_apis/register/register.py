import logging

from ..dependency.jwt_auth import get_hashed_password
from ..util.payloads import SignupOutput, UserInput
from ..util.set_session import get_session
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from e_commerce_api.e_commerce_db.models.models import Users
from ...e_commerce_db.models.enum import Role

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Register logging")

router = APIRouter(
    prefix="/signup",
    tags=["signup"],
    responses={
        404: {"description": "Not found"}
    }
)

register_roles = {
    "user": Role.User,
    "seller": Role.Seller
}


@router.put(
    "/{role_}",
    status_code=status.HTTP_200_OK,
    response_model=SignupOutput
)
async def sign_up(role_: str, creds_form: UserInput, session: Session = Depends(get_session)):
    if role_ not in register_roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown Role!")

    try:
        await find_user(creds_form, session)

        creds_form.password = get_hashed_password(creds_form.password)
        new_user = Users(**creds_form.dict(), role=register_roles.get(role_))
        session.add(new_user)
        session.commit()

        return SignupOutput(status_code=status.HTTP_200_OK)

    except HTTPException as error:
        if error.status_code == 400:
            raise error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error"
        )


async def find_user(creds_form, session):

    is_user = (
        session.query(Users)
        .filter(
            or_(
                Users.user_name == creds_form.user_name,
                Users.email == creds_form.email
            )
        )
        .first()
    )

    if not is_user:
        return

    logger.info(is_user.user_name)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Account already exist"
    )


