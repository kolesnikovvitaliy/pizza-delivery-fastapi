from fastapi import APIRouter

router = APIRouter(tags=["Orders"])


@router.get("/")
async def hello():
    return {"Hello, World!"}
