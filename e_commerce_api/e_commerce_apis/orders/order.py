import logging

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from e_commerce_api.e_commerce_apis.dependency.role_checker import user_pass
from e_commerce_api.e_commerce_apis.util.payloads import OrderPayload, OrderConfirmation
from e_commerce_api.e_commerce_apis.util.set_session import get_session
from e_commerce_api.e_commerce_db.models.models import Users, Orders, OrderItems, Products
from e_commerce_api.e_commerce_db.models.enum import OrderStatus
from e_commerce_api.e_commerce_apis.orders.orders_utli import gen_order_confirmation


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("order api")

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={
        404: {"description": "Not found"}
    }
)


@router.put(
    "/place_order",
    status_code=status.HTTP_200_OK,
    response_model=OrderConfirmation,
    dependencies=[Depends(user_pass)]
)
async def place_order(
        payload: OrderPayload, user: Users = Depends(user_pass), session: Session = Depends(get_session)
):
    quantity, total_amount = 0, 0

    for item in payload.product_ids:
        total_amount = total_amount + item[-1]
        quantity = quantity + item[1]

    logger.info(f"total_amount, quantity = ${total_amount}, {quantity}")

    try:
        new_order = Orders(
            user_id=user.id,
            order_date=datetime.utcnow(),
            total_amount=total_amount,
            status=OrderStatus.Placed.value,
            conformation_number=gen_order_confirmation()
        )
        session.add(new_order)

        for item in payload.product_ids:
            order_items = OrderItems(order_id=new_order.id, product_id=item[0], quantity=item[1], price=item[-1])
            product_quantity = session.query(Products).filter(product_id=item[0]).quantity_available
            product_quantity - item[1]
            session.add(order_items)

        session.commit()

        return OrderConfirmation(
            order_confirmation=new_order.conformation_number,
            status_code=status.HTTP_200_OK
        )

    except HTTPException as error:
        session.rollback()
        logger.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")




