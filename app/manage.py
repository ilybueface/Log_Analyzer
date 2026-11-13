from fastapi import FastAPI
from app.api.v1.endpoints.logs import router
from app.core.config import settings

app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "manage:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
