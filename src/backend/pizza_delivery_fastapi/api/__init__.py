from fastapi import APIRouter

from .v1.orders.views import router as router_orders
from .v1.products.views import router as products_router

router = APIRouter()

router.include_router(
    router=products_router,
    prefix="/products",
)

router.include_router(
    router=router_orders,
    prefix="/orders",
)
