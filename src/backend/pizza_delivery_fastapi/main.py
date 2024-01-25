import uvicorn


from fastapi import FastAPI
from .core.core_config import settings, core_logger as logger


from .auth import router as router_auth
from .api import router as router_v1


app = FastAPI(title="PIZZA_DELIVERY_FASTAPI")
app.include_router(router=router_auth)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
async def func():
    logger.info(f"request / endpoint!")
    return {"message": "hello world!"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
