import logging
from enum import Enum
from fastapi import HTTPException, APIRouter
from app.api.v1.endpoints.sources import source_to_mode
from app.schemas.log_schema import PerformanceCheckResponse
from app.services.log_service import get_single_sources, get_aggregated_sources

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class CheckStatus(str, Enum):
    ALL_SUCCESS = "all_success"
    PARTIAL_SUCCESS = "partial_success"
    ALL_FAILED = "all_failed"


@router.get("/check/{id}", response_model=PerformanceCheckResponse)
async def check_single_performance(id: int):
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


@router.get("/check", response_model=PerformanceCheckResponse)
async def check_performance():
    logger.info("Start checking all sources")
    results, total_time = await get_aggregated_sources()
    formatted_results: list[str] = []
    success_count = 0
    for item in results:
        if isinstance(item, Exception):
            formatted_results.append(f"error while polling the source: {item}")
        else:
            formatted_results.append(str(item))
            success_count += 1

    total_count = len(results)

    if total_count > 0 and success_count == total_count:
        status = CheckStatus.ALL_SUCCESS
    elif success_count > 0:
        status = CheckStatus.PARTIAL_SUCCESS
    else:
        status = CheckStatus.ALL_FAILED
    logger.info(
        f"Finished checking all sources in {total_time}s with status {status.value}"
    )

    return {
        "status": status.value,
        "execution_time_seconds": total_time,
        "results": formatted_results,
    }
