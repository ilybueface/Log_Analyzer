import asyncio
import time


async def fetch_source_async(number: int, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{number} completed in {delay} seconds"


def fetch_source_sync(id: int, delay: float) -> str:
    time.sleep(delay)
    return f"{id} completed in {delay} seconds"


async def get_aggregated_sources() -> tuple[list[str], float]:
    start_time = time.perf_counter()

    results = await asyncio.gather(
        fetch_source_async(1, 2.0),
        fetch_source_async(2, 2.5),
        fetch_source_async(3, 2.0),
        fetch_source_async(4, 1.5),
        fetch_source_async(5, 1.0),
        asyncio.to_thread(fetch_source_sync, 6, 2.0),
    )

    total_time = round(time.perf_counter() - start_time, 3)
    return results, total_time
