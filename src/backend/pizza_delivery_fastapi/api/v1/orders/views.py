from typing import List
from fastapi import APIRouter, Depends, status
from pizza_delivery_fastapi.api.v1.orders.dependencies import (
    get_order_by_id_admin,
    get_user_order_by_id,
)
from pizza_delivery_fastapi.api.v1.orders.schemas import (
    CreateOrder,
    OrderUpdate,
    ShowOrder,
    OrderUpdatePartial,
)
from pizza_delivery_fastapi.auth.jwt import (
    parse_jwt_admin_data,
    parse_jwt_user_data,
)
from pizza_delivery_fastapi.auth.schemas import JWTData
from pizza_delivery_fastapi.core.db import db_connect
from pizza_delivery_fastapi.core.models.order import Order
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud

router = APIRouter(tags=["Orders"])


@router.post(
    "/order",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowOrder,
)
async def create_order(
    order_in: CreateOrder,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    session: AsyncSession = Depends(db_connect),
) -> ShowOrder:
    """
    ## Placing an Order
    This requires the following
    - quantity : integer
    - pizza_name: str
    - pizza_size: str
    """
    return await crud.create_order(
        session=session,
        jwt_data=jwt_data,
        order_in=order_in,
    )


@router.get(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=List[ShowOrder],
)
async def admin_list_all_orders(
    jwt_data: JWTData = Depends(parse_jwt_admin_data),
    session: AsyncSession = Depends(db_connect),
) -> list[ShowOrder]:
    """
    ## List all orders
    This lists all  orders made. It can be accessed by superusers
    """
    return await crud.get_orders(session=session)


@router.get(
    "/order{order_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowOrder,
)
async def admin_get_order(
    order: ShowOrder = Depends(get_order_by_id_admin),
) -> ShowOrder:
    """
    ## Get an order by its ID
    This gets an order by its ID and is only accessed by a superuser
    """
    return order


@router.get(
    "/user/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=list[ShowOrder],
)
async def get_list_user_orders(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    session: AsyncSession = Depends(db_connect),
) -> list[ShowOrder]:
    """
    ## Get a current user's orders
    This lists the orders made by the currently logged in users
    """
    return await crud.get_user_orders(session=session, jwt_data=jwt_data)


@router.get(
    "/user/order{order_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowOrder,
)
async def get_user_order(
    order: ShowOrder = Depends(get_user_order_by_id),
) -> ShowOrder:
    """
    ## Get a specific order by the currently logged in user
    This returns an order by ID for the currently logged in user
    """
    return order


@router.put(
    "/order/update/{id}",
    response_model=ShowOrder,
)
async def admin_update_order_status(
    order_update: OrderUpdate,
    order: ShowOrder = Depends(get_order_by_id_admin),
    session: AsyncSession = Depends(db_connect),
) -> ShowOrder:
    """
    ## Update an order's status
    This is for updating an order's status and requires ` order_status ` in str format
    """
    return await crud.update_order_status(
        session=session,
        order=order,
        order_update=order_update,
    )


@router.patch(
    "/order/update/{id}",
    response_model=ShowOrder,
)
async def update_order_partial(
    order_update: OrderUpdatePartial,
    session: AsyncSession = Depends(db_connect),
    order: Order = Depends(get_user_order_by_id),
) -> ShowOrder:
    """
    ## Updating an order
    This updates an order and requires the following fields
    - quantity: integer
    - pizza_name: str
    - pizza_size: str
    """
    return await crud.update_order(
        session=session,
        order_update=order_update,
        partial=True,
        order=order,
    )


@router.delete("/order/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order: Order = Depends(get_user_order_by_id),
    session: AsyncSession = Depends(db_connect),
) -> None:
    """
    ## Delete an Order
    This deletes an order by its ID
    """
    await crud.delete_order(session=session, order=order)
