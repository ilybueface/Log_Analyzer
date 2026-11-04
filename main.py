import asyncio
import time
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
app = FastAPI()


async def fetch_source_async(number: int, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{number} completed in {delay} seconds"


def fetch_source_sync(number: int, delay: float) -> str:
    time.sleep(delay)
    return f"{number} completed in {delay} seconds"


@app.get("/check")
async def check_performance():
    logger.info("Start checking")
    start_time = time.perf_counter()

    results = await asyncio.gather(
        fetch_source_async(1, 3.0),
        fetch_source_async(2, 2.5),
        fetch_source_async(3, 2.0),
        fetch_source_async(4, 1.5),
        fetch_source_async(5, 1.0),
        asyncio.to_thread(fetch_source_sync, 6, 2),
    )

    end_time = time.perf_counter()
    total_time = end_time - start_time

    return {
        "status": "success",
        "execution_time_seconds": total_time,
        "results": results,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
