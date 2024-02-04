import uvicorn
from fastapi import FastAPI

from .api import router as router_v1
from .auth import router as router_auth
# from .core.core_config import core_logger as logger
from .core.core_config import settings

app = FastAPI(title="PIZZA_DELIVERY_FASTAPI")
app.include_router(router=router_auth)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
