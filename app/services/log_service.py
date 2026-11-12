import asyncio
import time
from typing import Any
from app.api.v1.endpoints.sources import source_to_mode


async def fetch_source_async(number: int, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{number} completed in {delay} seconds"


def fetch_source_sync(id: int, delay: float) -> str:
    time.sleep(delay)
    return f"{id} completed in {delay} seconds"


def create_source_task(source_id: int, param: dict[str, Any]) -> Any:
    delay = param.get("delay_seconds", 0.0)
    if param.get("is_async"):
        return fetch_source_async(source_id, delay)
    return asyncio.to_thread(fetch_source_sync, source_id, delay)


async def get_aggregated_sources() -> tuple[list[str], float]:
    start_time = time.perf_counter()

    tasks = [
        create_source_task(source, param) for source, param in source_to_mode.items()
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    total_time = round(time.perf_counter() - start_time, 3)
    return results, total_time


async def get_single_sources(source_id: int) -> tuple[list[str], float]:
    start_time = time.perf_counter()
    param = source_to_mode[source_id]
    task = create_source_task(source_id, param)
    results = await task
    total_time = round(time.perf_counter() - start_time, 3)
    return [results], total_time
