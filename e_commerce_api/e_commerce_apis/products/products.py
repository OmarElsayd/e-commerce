import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from e_commerce_api.e_commerce_apis.dependency.role_checker import user_pass, admin_pass, seller_pass
from e_commerce_api.e_commerce_apis.util.payloads import ProductInputForm
from e_commerce_api.e_commerce_apis.util.set_session import get_session
from e_commerce_api.e_commerce_db.models.models import Users, Products, Category

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("products api")

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={
        404: {"description": "Not found"}
    }
)


@router.put(
    "/add_category",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_pass)]
)
async def add_category(name: str, session: Session = Depends(get_session)):
    cat_name = name.capitalize()
    is_cat = session.query(Category).filter(Category.name == cat_name).first()

    if is_cat:
        logger.info("already exist")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{cat_name} Category already exist")

    new_cat = Category(name=cat_name)
    session.add(new_cat)
    logger.info("Adding new Category")

    session.commit()
    logger.info("Adding Category has been completed")

    return {
        "status_code": status.HTTP_200_OK,
        "message": "Category has been added"
    }


@router.delete(
    "/delete_category",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_pass)]
)
def delete_category(category: str, session: Session = Depends(get_session)):
    try:
        is_category = session.query(Category).filter(name=category).first()

        if not is_category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category Does not exist")

        logger.info("found category")
        session.delete(is_category)
        logger.info("Deleting category")
        session.commit()

    except HTTPException as error:
        logger.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    return {"status_code": status.HTTP_200_OK}


@router.get(
    "/get_all_category",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(user_pass)]
)
def get_all_cat(session: Session = Depends(get_session)):
    return session.query(Category).all()


@router.put(
    "/add_product",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(seller_pass)]
)
async def add_product(form: ProductInputForm = Depends(), session: Session = Depends(get_session)):
    try:
        product_payload = Products(
            name=form.name,
            description=form.description,
            price=form.price,
            quantity_available=form.quantity_available,
            category_id=form.category_id,
            image_url=form.image_url
        )

        logger.debug("Product payload has been established")

        session.add(product_payload)
        session.commit()

        logger.info("New product has been added to the database")

        return status.HTTP_200_OK

    except HTTPException as error:
        logger.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="500_INTERNAL_SERVER_ERROR")
