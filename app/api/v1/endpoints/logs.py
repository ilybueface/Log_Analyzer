import logging
from fastapi import APIRouter, HTTPException
from app.schemas.log_schema import (
    PerformanceCheckResponse,
    PerformanceCheckSingleResponse,
    CheckStatus,
    SingleStatusCheck,
)
from app.services.log_service import get_single_sources, get_aggregated_sources
from app.core.exceptions import SourceNumberNotFoundError
from app.api.v1.dependencies import SettingsDependency

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/performance", tags=["sources"])


@router.get("/check/{id}", response_model=PerformanceCheckSingleResponse)
async def check_single_performance(id: int, settings: SettingsDependency):
    logger.info("Start checking")
    try:
        results, total_time = await get_single_sources(id, settings)
        if isinstance(results, Exception):
            status = SingleStatusCheck.FAILED
            formatted_result = f"error while polling the source: {results}"
        else:
            status = SingleStatusCheck.SUCCESS
            formatted_result = str(results)
    except SourceNumberNotFoundError:
        raise HTTPException(status_code=404, detail=f"the source number {id} not found")

    logger.info(
        f"Finished checking source {id} in {total_time}s with status {status.value}"
    )
    return {
        "status": status.value,
        "execution_time_seconds": total_time,
        "results": [formatted_result],
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
