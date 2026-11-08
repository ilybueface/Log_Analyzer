import logging
from fastapi import HTTPException, APIRouter, status
from app.schemas.log_schema import PerformanceCheckResponse
from app.services.log_service import get_aggregated_sources

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/check/{id}", response_model=PerformanceCheckResponse)
async def check_performance(id: int):
    if id not in :
        raise HTTPException(
            status_code=404,
            detail='Not it found'
        )
    logger.info("Start checking")

    results, total_time = await get_aggregated_sources()

    logger.info(f"Finished checking in {total_time}s")
    return {
        "status": "success",
        "execution_time_seconds": total_time,
        "results": results,
    }
