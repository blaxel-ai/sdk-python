import asyncio
import time
from collections import Counter

from blaxel.client import client
from blaxel.common.settings import settings


async def request_agent(name):
    response = await client.get_async_httpx_client().get(
        f"{settings.run_url}/{settings.workspace}/agents/{name}"
    )
    if response.status_code != 200:
        raise Exception(f"Agent {name} returned status code {response.status_code} with body {response.text}")
    return response.status_code

async def main():
    number_of_calls = 500
    batch_size = 100
    agent_name = "agent-telemetry-ts"

    total_start_time = time.time()
    batch_times = []

    for batch_start in range(0, number_of_calls, batch_size):
        batch_end = min(batch_start + batch_size, number_of_calls)
        batch_tasks = [request_agent(agent_name) for _ in range(batch_start, batch_end)]
        print(f"Processing batch {batch_start//batch_size + 1} ({batch_start}-{batch_end-1})")

        batch_start_time = time.time()
        status_codes = await asyncio.gather(*batch_tasks)
        batch_time = time.time() - batch_start_time
        batch_times.append(batch_time)

        status_counts = Counter(status_codes)
        print(f"Completed batch {batch_start//batch_size + 1}")
        print(f"Status codes: {dict(status_counts)}")
        print(f"Batch time: {batch_time:.2f}s")
        print(f"Mean time per request in batch: {batch_time/batch_size:.3f}s")
        print("-" * 50)

    total_time = time.time() - total_start_time
    mean_time_per_request = total_time / number_of_calls

    print("\nSummary:")
    print(f"Total execution time: {total_time:.2f}s")
    print(f"Mean time per request: {mean_time_per_request:.3f}s")
    print(f"Fastest batch: {min(batch_times):.2f}s")
    print(f"Slowest batch: {max(batch_times):.2f}s")
    print(f"Average batch time: {sum(batch_times)/len(batch_times):.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
