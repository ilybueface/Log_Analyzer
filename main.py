import asyncio
import time


async def fetch_source_async(number: int, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{number} completed in {delay} seconds"


def fetch_source_sync(number: int, delay: float) -> str:
    time.sleep(delay)
    return f"{number} completed in {delay} seconds"


async def main():
    start_time = time.perf_counter()
    print("Start checking")

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

    print("\nResults")
    for r in results:
        print(r)

    print(f"the program's execution time was: {total_time}")


if __name__ == "__main__":
    asyncio.run(main())
