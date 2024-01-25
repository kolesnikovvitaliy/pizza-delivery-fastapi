import uvicorn
from backend_config.environments import PORT, HOST


if __name__ == "__main__":
    uvicorn.run(
        "pizza_delivery_fastapi.main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="debug",
    )
