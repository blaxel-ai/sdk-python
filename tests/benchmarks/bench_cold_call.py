"""Cold-call benchmark: create → call → delete.

Measures end-to-end latency of sandbox lifecycle operations with
per-phase breakdown (create / call / delete).

Usage:
    python -m tests.benchmarks.bench_cold_call
    python -m tests.benchmarks.bench_cold_call --iterations 5 --warmup 0
"""

import argparse
import asyncio
import statistics
import time
from dataclasses import dataclass, field

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, default_region, unique_name

ITERATIONS = 10
WARMUP_ITERATIONS = 1


@dataclass
class Timing:
    total: float = 0.0
    create: float = 0.0
    call: float = 0.0
    delete: float = 0.0


async def bench_cold_ls(iteration: int) -> Timing:
    """create -> fs.ls('/') -> delete"""
    name = unique_name("bench-cold-ls")
    t = Timing()

    t0 = time.perf_counter()
    sandbox = await SandboxInstance.create({
        "name": name,
        "image": default_image,
        "labels": default_labels,
        "memory": 2048,
        "region": default_region,
    })
    t1 = time.perf_counter()
    t.create = t1 - t0

    await sandbox.fs.ls("/")
    t2 = time.perf_counter()
    t.call = t2 - t1

    try:
        await SandboxInstance.delete(name)
    except Exception:
        pass
    t3 = time.perf_counter()
    t.delete = t3 - t2

    t.total = t3 - t0
    return t


async def bench_cold_exec(iteration: int) -> Timing:
    """create -> process.exec('echo ok') -> delete"""
    name = unique_name("bench-cold-exec")
    t = Timing()

    t0 = time.perf_counter()
    sandbox = await SandboxInstance.create({
        "name": name,
        "image": default_image,
        "labels": default_labels,
        "memory": 2048,
        "region": default_region,
    })
    t1 = time.perf_counter()
    t.create = t1 - t0

    await sandbox.process.exec({
        "command": "echo ok",
        "wait_for_completion": True,
    })
    t2 = time.perf_counter()
    t.call = t2 - t1

    try:
        await SandboxInstance.delete(name)
    except Exception:
        pass
    t3 = time.perf_counter()
    t.delete = t3 - t2

    t.total = t3 - t0
    return t


def fmt(seconds: float) -> str:
    return f"{seconds * 1000:.0f}ms"


def format_stats(values: list[float], label: str) -> str:
    if not values:
        return f"  {label}: no data"
    mean = statistics.mean(values)
    med = statistics.median(values)
    mn = min(values)
    mx = max(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    return (
        f"  {label:16s}  "
        f"mean={fmt(mean):>7s}  med={fmt(med):>7s}  "
        f"min={fmt(mn):>7s}  max={fmt(mx):>7s}  std={fmt(std):>7s}"
    )


async def run_benchmark(
    name: str,
    fn,
    iterations: int,
    warmup: int,
) -> list[Timing]:
    print(f"\n{'='*80}")
    print(f"  {name}")
    print(f"{'='*80}")

    if warmup > 0:
        print(f"  warming up ({warmup} iteration{'s' if warmup > 1 else ''})...")
        for i in range(warmup):
            try:
                await fn(i)
            except Exception as e:
                print(f"  warmup {i+1} failed: {e}")

    timings: list[Timing] = []
    for i in range(iterations):
        try:
            t = await fn(i)
            timings.append(t)
            print(
                f"  [{i+1:>2}/{iterations}] "
                f"total={fmt(t.total):>7s}  "
                f"create={fmt(t.create):>7s}  "
                f"call={fmt(t.call):>7s}  "
                f"delete={fmt(t.delete):>7s}"
            )
        except Exception as e:
            print(f"  [{i+1:>2}/{iterations}] FAILED: {e}")

    if timings:
        print()
        print(format_stats([t.total for t in timings], "total"))
        print(format_stats([t.create for t in timings], "create"))
        print(format_stats([t.call for t in timings], "call"))
        print(format_stats([t.delete for t in timings], "delete"))
    return timings


async def main(iterations: int, warmup: int) -> None:
    print(f"\nCold-call benchmark (create -> call -> delete)")
    print(f"  iterations={iterations}, warmup={warmup}")
    print(f"  image={default_image}, region={default_region}")

    ls_timings = await run_benchmark(
        "create -> fs.ls('/') -> delete",
        bench_cold_ls,
        iterations,
        warmup,
    )

    exec_timings = await run_benchmark(
        "create -> process.exec('echo ok') -> delete",
        bench_cold_exec,
        iterations,
        warmup,
    )

    print(f"\n{'='*80}")
    print("  SUMMARY")
    print(f"{'='*80}")
    if ls_timings:
        print("  fs.ls:")
        print(format_stats([t.total for t in ls_timings], "total"))
        print(format_stats([t.create for t in ls_timings], "create"))
        print(format_stats([t.call for t in ls_timings], "call"))
        print(format_stats([t.delete for t in ls_timings], "delete"))
    if exec_timings:
        print("  process.exec:")
        print(format_stats([t.total for t in exec_timings], "total"))
        print(format_stats([t.create for t in exec_timings], "create"))
        print(format_stats([t.call for t in exec_timings], "call"))
        print(format_stats([t.delete for t in exec_timings], "delete"))
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cold-call sandbox benchmark")
    parser.add_argument("--iterations", type=int, default=ITERATIONS)
    parser.add_argument("--warmup", type=int, default=WARMUP_ITERATIONS)
    args = parser.parse_args()

    asyncio.run(main(args.iterations, args.warmup))
