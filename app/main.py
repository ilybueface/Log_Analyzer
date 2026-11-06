import logging
from fastapi import FastAPI
from app.schemas.log_schema import PerformanceCheckResponse
from app.services.log_service import get_aggregated_sources

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/check", response_model=PerformanceCheckResponse)
async def check_performance():
    logger.info("Start checking")

    results, total_time = await get_aggregated_sources()

    logger.info(f"Finished checking in {total_time}s")
    return {
        "status": "success",
        "execution_time_seconds": total_time,
        "results": results,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
