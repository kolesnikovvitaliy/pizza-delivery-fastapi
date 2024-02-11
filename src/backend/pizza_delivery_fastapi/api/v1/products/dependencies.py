from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from pizza_delivery_fastapi.auth.jwt import parse_jwt_user_data
from pizza_delivery_fastapi.auth.schemas import JWTData
from sqlalchemy.ext.asyncio import AsyncSession
from pizza_delivery_fastapi.core.db import db_connect
from pizza_delivery_fastapi.core.models import Product
from . import crud


async def product_by_id(
    product_id: Annotated[int, Path],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    session: AsyncSession = Depends(db_connect),
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!",
    )
