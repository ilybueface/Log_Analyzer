import asyncio
import time
from typing import Any
from app.api.v1.endpoints.sources import source_to_mode
from app.core.exceptions import SourceNumberNotFoundError, SourceTimeoutError


async def fetch_source_async(number: int, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{number} completed in {delay} seconds"


def fetch_source_sync(id: int, delay: float) -> str:
    time.sleep(delay)
    return f"{id} completed in {delay} seconds"


def create_source_task(source_id, param: dict[str, Any]) -> Any:
    delay = param.get("delay_seconds", 0.0)
    if param.get("is_async"):
        return fetch_source_async(source_id, delay)
    return asyncio.to_thread(fetch_source_sync, source_id, delay)


async def poll_source(source_id: int, param: dict[str, Any], timeout: float) -> str:
    try:
        return await asyncio.wait_for(
            create_source_task(source_id, param),
            timeout=timeout,
        )
    except TimeoutError:
        raise SourceTimeoutError(
            f"Source {source_id} exceeded the timeout ({timeout} sec.)"
        ) from None


async def get_aggregated_sources(
    timeout: float,
) -> tuple[list[str | BaseException], float]:
    start_time = time.perf_counter()

    tasks = [
        poll_source(source, param, timeout) for source, param in source_to_mode.items()
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    total_time = round(time.perf_counter() - start_time, 3)
    return results, total_time


async def get_single_sources(
    source_id: int, timeout: float
) -> tuple[str | Exception, float]:
    if source_id not in source_to_mode:
        raise SourceNumberNotFoundError(f"Source {source_id} not found")
    start_time = time.perf_counter()
    param = source_to_mode[source_id]
    try:
        result = await poll_source(source_id, param, timeout)
    except Exception as err:
        result = err
    total_time = round(time.perf_counter() - start_time, 3)
    return result, total_time
