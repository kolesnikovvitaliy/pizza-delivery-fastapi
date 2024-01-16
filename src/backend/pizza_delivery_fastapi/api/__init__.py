from fastapi import APIRouter

from .v1.orders.views import router as router_orders


router = APIRouter()

router.include_router(
    router=router_orders,
    prefix="/orders",
)
