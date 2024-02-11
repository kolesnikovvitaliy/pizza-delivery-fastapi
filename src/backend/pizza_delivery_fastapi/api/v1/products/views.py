from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pizza_delivery_fastapi.core.db import db_connect
from pizza_delivery_fastapi.auth.jwt import (
    parse_jwt_admin_data,
    parse_jwt_user_data,
)
from pizza_delivery_fastapi.auth.schemas import JWTData
from . import crud
from .schemas import (
    Product,
    ProductCreate,
    ProductUpdatePartial,
    ProductUpdate
)
from .dependencies import product_by_id

router = APIRouter(tags=["Pizza"])


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def product_create_admin(
    product_in: ProductCreate,
    jwt_data: JWTData = Depends(parse_jwt_admin_data),
    session: AsyncSession = Depends(db_connect),
):
    return await crud.product_create(session=session, product_in=product_in)


@router.get("/", response_model=list[Product])
async def get_products(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    session: AsyncSession = Depends(db_connect),
):
    return await crud.get_products(session=session)


@router.get("/{product_id}", response_model=Product)
async def get_product(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    product: Product = Depends(product_by_id),
):
    return product


@router.put("/{product_id}")
async def update_product(
    product_update: ProductUpdate,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_connect),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{product_id}")
async def update_product_partial(
    product_update: ProductUpdatePartial,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_connect),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_connect),
) -> None:
    await crud.delete_product(session=session, product=product)
