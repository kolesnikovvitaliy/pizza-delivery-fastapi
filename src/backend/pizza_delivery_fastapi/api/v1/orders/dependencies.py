from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from pizza_delivery_fastapi.auth.jwt import (
    parse_jwt_admin_data,
    parse_jwt_user_data,
)
from pizza_delivery_fastapi.auth.schemas import JWTData
from sqlalchemy.ext.asyncio import AsyncSession
from pizza_delivery_fastapi.core.models import Order
from pizza_delivery_fastapi.core.db import db_connect
from . import crud


async def get_order_by_id_admin(
    order_id: Annotated[int, Path],
    jwt_data: JWTData = Depends(parse_jwt_admin_data),
    session: AsyncSession = Depends(db_connect),
) -> Order | None:
    order = await crud.get_order(session=session, order_id=order_id)
    if order is not None:
        return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order {order_id} not found",
    )


async def get_user_order_by_id(
    order_id: Annotated[int, Path],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    session: AsyncSession = Depends(db_connect),
) -> Order | None:
    order = await crud.get_user_order(
        session=session, order_id=order_id, jwt_data=jwt_data
    )
    if order is not None:
        return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order {order_id} not found",
    )
