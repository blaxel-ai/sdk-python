import asyncio
import statistics
import time

from utils import create_or_get_sandbox

from blaxel.core.sandbox.default import SandboxInstance
from blaxel.core.sandbox.default.action import SandboxAction

SANDBOX_NAME = "fs-ls-benchmark"
NUM_ITERATIONS = 100


async def benchmark_fs_ls(sandbox: SandboxInstance, num_iterations: int = NUM_ITERATIONS):
    """Benchmark fs.ls performance with connection reuse."""
    print(f"\n{'=' * 60}")
    print(f"Benchmarking fs.ls with {num_iterations} iterations")
    print(f"{'=' * 60}\n")

    # Warm up - first request may be slower due to connection setup
    print("Warming up (first request)...")
    start = time.perf_counter()
    await sandbox.fs.ls("/")
    warmup_time = (time.perf_counter() - start) * 1000
    print(f"  Warmup request: {warmup_time:.2f}ms\n")

    # Run benchmark
    print(f"Running {num_iterations} fs.ls requests...")
    times_ms = []

    for i in range(num_iterations):
        start = time.perf_counter()
        await sandbox.fs.ls("/")
        elapsed_ms = (time.perf_counter() - start) * 1000
        times_ms.append(elapsed_ms)

        # Progress indicator every 10 iterations
        if (i + 1) % 10 == 0:
            print(f"  Completed {i + 1}/{num_iterations} requests...")

    # Calculate statistics
    total_time = sum(times_ms)
    avg_time = statistics.mean(times_ms)
    median_time = statistics.median(times_ms)
    min_time = min(times_ms)
    max_time = max(times_ms)
    std_dev = statistics.stdev(times_ms) if len(times_ms) > 1 else 0

    # Percentiles
    sorted_times = sorted(times_ms)
    p50 = sorted_times[int(len(sorted_times) * 0.50)]
    p90 = sorted_times[int(len(sorted_times) * 0.90)]
    p95 = sorted_times[int(len(sorted_times) * 0.95)]
    p99 = sorted_times[int(len(sorted_times) * 0.99)]

    print(f"\n{'=' * 60}")
    print("RESULTS")
    print(f"{'=' * 60}")
    print(f"Total requests:     {num_iterations}")
    print(f"Total time:         {total_time:.2f}ms ({total_time / 1000:.2f}s)")
    print(f"Requests/second:    {num_iterations / (total_time / 1000):.2f}")
    print()
    print(f"Average:            {avg_time:.2f}ms")
    print(f"Median:             {median_time:.2f}ms")
    print(f"Min:                {min_time:.2f}ms")
    print(f"Max:                {max_time:.2f}ms")
    print(f"Std Dev:            {std_dev:.2f}ms")
    print()
    print("Percentiles:")
    print(f"  p50:              {p50:.2f}ms")
    print(f"  p90:              {p90:.2f}ms")
    print(f"  p95:              {p95:.2f}ms")
    print(f"  p99:              {p99:.2f}ms")
    print(f"{'=' * 60}\n")

    return {
        "total_requests": num_iterations,
        "total_time_ms": total_time,
        "requests_per_second": num_iterations / (total_time / 1000),
        "avg_ms": avg_time,
        "median_ms": median_time,
        "min_ms": min_time,
        "max_ms": max_time,
        "std_dev_ms": std_dev,
        "p50_ms": p50,
        "p90_ms": p90,
        "p95_ms": p95,
        "p99_ms": p99,
        "all_times_ms": times_ms,
    }


async def benchmark_concurrent_fs_ls(
    sandbox: SandboxInstance, num_concurrent: int = 10, num_batches: int = 10
):
    """Benchmark concurrent fs.ls requests."""
    print(f"\n{'=' * 60}")
    print("Benchmarking CONCURRENT fs.ls")
    print(
        f"  {num_concurrent} concurrent requests x {num_batches} batches = {num_concurrent * num_batches} total"
    )
    print(f"{'=' * 60}\n")

    all_times_ms = []

    for batch in range(num_batches):
        start = time.perf_counter()
        # Run concurrent requests
        await asyncio.gather(*[sandbox.fs.ls("/") for _ in range(num_concurrent)])
        batch_time_ms = (time.perf_counter() - start) * 1000
        all_times_ms.append(batch_time_ms)
        print(
            f"  Batch {batch + 1}/{num_batches}: {batch_time_ms:.2f}ms for {num_concurrent} concurrent requests"
        )

    total_requests = num_concurrent * num_batches
    total_time = sum(all_times_ms)
    avg_batch_time = statistics.mean(all_times_ms)

    print(f"\n{'=' * 60}")
    print("CONCURRENT RESULTS")
    print(f"{'=' * 60}")
    print(f"Total requests:     {total_requests}")
    print(f"Total time:         {total_time:.2f}ms ({total_time / 1000:.2f}s)")
    print(f"Requests/second:    {total_requests / (total_time / 1000):.2f}")
    print(f"Avg batch time:     {avg_batch_time:.2f}ms (for {num_concurrent} concurrent)")
    print(f"Avg per request:    {avg_batch_time / num_concurrent:.2f}ms (effective)")
    print(f"{'=' * 60}\n")

    return {
        "total_requests": total_requests,
        "total_time_ms": total_time,
        "requests_per_second": total_requests / (total_time / 1000),
        "avg_batch_time_ms": avg_batch_time,
        "effective_per_request_ms": avg_batch_time / num_concurrent,
    }


async def main():
    print("Starting fs.ls benchmark test")
    print("This will test HTTP client connection reuse performance\n")

    sandbox = await create_or_get_sandbox(SANDBOX_NAME)
    print(f"Using sandbox: {SANDBOX_NAME}")

    try:
        # Sequential benchmark
        sequential_results = await benchmark_fs_ls(sandbox, NUM_ITERATIONS)

        # Concurrent benchmark
        concurrent_results = await benchmark_concurrent_fs_ls(
            sandbox, num_concurrent=10, num_batches=10
        )

        # Summary
        print(f"\n{'=' * 60}")
        print("SUMMARY")
        print(f"{'=' * 60}")
        print(f"Sequential ({NUM_ITERATIONS} requests):")
        print(f"  - {sequential_results['requests_per_second']:.2f} req/s")
        print(f"  - {sequential_results['avg_ms']:.2f}ms avg latency")
        print()
        print("Concurrent (10 concurrent x 10 batches = 100 requests):")
        print(f"  - {concurrent_results['requests_per_second']:.2f} req/s")
        print(f"  - {concurrent_results['effective_per_request_ms']:.2f}ms effective latency")
        print(f"{'=' * 60}")

    finally:
        # Cleanup clients
        await SandboxAction.close_all_clients()
        print("\nClosed all HTTP clients")


if __name__ == "__main__":
    asyncio.run(main())
