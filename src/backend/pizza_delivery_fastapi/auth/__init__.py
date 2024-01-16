from fastapi import APIRouter

from .views import router as router_auth


router = APIRouter()

router.include_router(router=router_auth)
