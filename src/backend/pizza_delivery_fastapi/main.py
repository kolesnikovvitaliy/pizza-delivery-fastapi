import uvicorn


from fastapi import FastAPI


from .auth import router as router_auth
from .api import router as router_v1


app = FastAPI(title="PIZZA_DELIVERY_FASTAPI")
app.include_router(router=router_auth)
app.include_router(router=router_v1, prefix="/api_v1")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
