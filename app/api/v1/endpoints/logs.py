import logging
from fastapi import HTTPException, APIRouter
from app.api.v1.endpoints.sources import source_to_mode
from app.schemas.log_schema import PerformanceCheckResponse
from app.services.log_service import get_single_sources

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/check/{id}", response_model=PerformanceCheckResponse)
async def check_performance(id: int):
    if id not in source_to_mode:
        raise HTTPException(status_code=404, detail="Not it found")
    logger.info("Start checking")

    results, total_time = await get_single_sources(id)

    logger.info(f"Finished checking source {id} in {total_time}s")
    return {
        "status": "success",
        "execution_time_seconds": total_time,
        "results": results,
    }
