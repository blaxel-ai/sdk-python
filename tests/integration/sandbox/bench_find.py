import asyncio
import statistics
import time
from typing import Any, Dict, List

from blaxel.core.sandbox import SandboxInstance

# ============ CONFIGURATION ============
ITERATIONS_PER_TEST = 20
WARMUP_ITERATIONS = 3
SANDBOX_NAME = "fzf-test"
REPO_URL = "https://github.com/vercel/next.js.git"
REPO_PATH = "/workspace/nextjs-repo"
SETUP_ENVIRONMENT = True
# =======================================


async def setup_environment(sandbox: SandboxInstance) -> None:
    """Setup test environment with Next.js repo."""
    print("📦 Setting up environment...")

    print("   Installing fd...")
    await sandbox.process.exec(
        {
            "command": "curl -L https://github.com/sharkdp/fd/releases/download/v10.2.0/fd-v10.2.0-x86_64-unknown-linux-musl.tar.gz | tar xz && mv fd-v10.2.0-x86_64-unknown-linux-musl/fd /usr/local/bin/fd",
            "waitForCompletion": True,
        }
    )

    print(f"   Cloning {REPO_URL}...")
    await sandbox.process.exec(
        {
            "command": f"git clone --depth 1 {REPO_URL} {REPO_PATH}",
            "waitForCompletion": True,
        }
    )

    print("   Running npm install...")
    await sandbox.process.exec(
        {
            "command": f"cd {REPO_PATH} && npm install",
            "waitForCompletion": True,
        }
    )

    print("✓ Environment ready")


async def bench_find_bash(sandbox: SandboxInstance) -> Dict[str, Any]:
    """Benchmark bash find command."""
    start = time.time()

    result = await sandbox.process.exec(
        {
            "command": f'find {REPO_PATH} -type f \\( -name "*.json" -o -name "*.html" \\) | head -1000',
            "waitForCompletion": True,
        }
    )

    duration = (time.time() - start) * 1000  # Convert to ms
    output = result.logs or ""
    lines = [line for line in output.strip().split("\n") if line]
    file_count = len(lines)

    return {
        "method": "find-bash",
        "duration": duration,
        "file_count": file_count,
        "success": True,
    }


async def bench_fd(sandbox: SandboxInstance) -> Dict[str, Any]:
    """Benchmark fd (Rust find alternative)."""
    start = time.time()

    result = await sandbox.process.exec(
        {
            "command": f"fd -t f -e json -e html . {REPO_PATH} | head -1000",
            "waitForCompletion": True,
        }
    )

    duration = (time.time() - start) * 1000  # Convert to ms
    output = result.logs or ""
    lines = [line for line in output.strip().split("\n") if line]
    file_count = len(lines)

    return {
        "method": "fd",
        "duration": duration,
        "file_count": file_count,
        "success": True,
    }


async def bench_native_find(sandbox: SandboxInstance) -> Dict[str, Any]:
    """Benchmark native find method."""
    start = time.time()

    result = await sandbox.fs.find(
        REPO_PATH,
        type="file",
        patterns=["*.json", "*.html"],
        max_results=1000,
    )

    duration = (time.time() - start) * 1000  # Convert to ms
    file_count = len(result.matches) if result.matches else 0

    return {
        "method": "native-find",
        "duration": duration,
        "file_count": file_count,
        "success": True,
    }


def calculate_stats(results: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate statistics from benchmark results."""
    durations = [r["duration"] for r in results if r["success"]]
    file_counts = [r["file_count"] for r in results if r["success"]]

    durations_sorted = sorted(durations)

    return {
        "avg": statistics.mean(durations) if durations else 0,
        "min": min(durations) if durations else 0,
        "max": max(durations) if durations else 0,
        "p50": durations_sorted[len(durations_sorted) // 2] if durations_sorted else 0,
        "p95": durations_sorted[int(len(durations_sorted) * 0.95)] if durations_sorted else 0,
        "p99": durations_sorted[int(len(durations_sorted) * 0.99)] if durations_sorted else 0,
        "avg_file_count": statistics.mean(file_counts) if file_counts else 0,
        "success_rate": (len([r for r in results if r["success"]]) / len(results)) * 100
        if results
        else 0,
    }


async def main():
    """Main benchmark function."""
    print("========================================")
    print("  BASH FIND vs FD vs NATIVE FIND")
    print("  BENCHMARK (Python SDK)")
    print("========================================")
    print("\n⚙️  Configuration:")
    print(f"   Sandbox: {SANDBOX_NAME}")
    print(f"   Repository: {REPO_URL}")
    print(f"   Path: {REPO_PATH}")
    print(f"   Iterations: {ITERATIONS_PER_TEST}")
    print(f"   Warmup: {WARMUP_ITERATIONS}\n")

    try:
        print(f"🔗 Connecting to sandbox: {SANDBOX_NAME}...")
        sandbox = await SandboxInstance.get(SANDBOX_NAME)
        print("✓ Connected\n")

        if SETUP_ENVIRONMENT:
            try:
                await setup_environment(sandbox)
            except Exception as e:
                print(f"⚠️  Setup failed: {e}")

        # Validation
        print("\n🔍 Validation...")

        bash_val = await sandbox.process.exec(
            {
                "command": f'find {REPO_PATH} -type f \\( -name "*.json" -o -name "*.html" \\) | head -100 | wc -l',
                "waitForCompletion": True,
            }
        )
        bash_count = int((bash_val.logs or "").strip()) if bash_val.logs else 0
        print(f"   find-bash: {bash_count} files")

        fd_val = await sandbox.process.exec(
            {
                "command": f"fd -t f -e json -e html . {REPO_PATH} | head -100 | wc -l",
                "waitForCompletion": True,
            }
        )
        fd_count = int((fd_val.logs or "").strip()) if fd_val.logs else 0
        print(f"   fd:        {fd_count} files")

        native_val = await sandbox.fs.find(
            REPO_PATH,
            type="file",
            patterns=["*.json", "*.html"],
            max_results=100,
        )
        print(f"   native:    {len(native_val.matches) if native_val.matches else 0} matches")
        if native_val.matches:
            print("   Sample files:")
            for m in native_val.matches[:3]:
                print(f"     - {m.path} ({m.type_})")

        all_results: List[Dict[str, Any]] = []

        # Warmup
        print(f"\n🔥 Warmup ({WARMUP_ITERATIONS} iterations)...")
        for i in range(WARMUP_ITERATIONS):
            await bench_find_bash(sandbox)
            await bench_fd(sandbox)
            await bench_native_find(sandbox)
        print("✓ Warmup complete")

        # Benchmark find-bash
        print(f"\n📊 Benchmarking find-bash ({ITERATIONS_PER_TEST} iterations)...")
        for i in range(ITERATIONS_PER_TEST):
            result = await bench_find_bash(sandbox)
            all_results.append(result)
            if (i + 1) % 5 == 0:
                print(f"   Progress: {i + 1}/{ITERATIONS_PER_TEST}")

        # Benchmark fd
        print(f"\n📊 Benchmarking fd ({ITERATIONS_PER_TEST} iterations)...")
        for i in range(ITERATIONS_PER_TEST):
            result = await bench_fd(sandbox)
            all_results.append(result)
            if (i + 1) % 5 == 0:
                print(f"   Progress: {i + 1}/{ITERATIONS_PER_TEST}")

        # Benchmark native-find
        print(f"\n📊 Benchmarking native-find ({ITERATIONS_PER_TEST} iterations)...")
        for i in range(ITERATIONS_PER_TEST):
            result = await bench_native_find(sandbox)
            all_results.append(result)
            if (i + 1) % 5 == 0:
                print(f"   Progress: {i + 1}/{ITERATIONS_PER_TEST}")

        # Calculate statistics
        bash_results = [r for r in all_results if r["method"] == "find-bash"]
        fd_results = [r for r in all_results if r["method"] == "fd"]
        native_results = [r for r in all_results if r["method"] == "native-find"]

        bash_stats = calculate_stats(bash_results)
        fd_stats = calculate_stats(fd_results)
        native_stats = calculate_stats(native_results)

        # Display results
        print("\n\n========================================")
        print("           RESULTS")
        print("========================================\n")

        print(
            "Method        | Avg (ms) | Min (ms) | Max (ms) | P50 (ms) | P95 (ms) | P99 (ms) | Avg Files | Success"
        )
        print(
            "--------------|----------|----------|----------|----------|----------|----------|-----------|--------"
        )

        print(
            f"find-bash     | {bash_stats['avg']:8.1f} | {bash_stats['min']:8.1f} | {bash_stats['max']:8.1f} | {bash_stats['p50']:8.1f} | {bash_stats['p95']:8.1f} | {bash_stats['p99']:8.1f} | {bash_stats['avg_file_count']:9.1f} | {bash_stats['success_rate']:.0f}%"
        )
        print(
            f"fd            | {fd_stats['avg']:8.1f} | {fd_stats['min']:8.1f} | {fd_stats['max']:8.1f} | {fd_stats['p50']:8.1f} | {fd_stats['p95']:8.1f} | {fd_stats['p99']:8.1f} | {fd_stats['avg_file_count']:9.1f} | {fd_stats['success_rate']:.0f}%"
        )
        print(
            f"native-find   | {native_stats['avg']:8.1f} | {native_stats['min']:8.1f} | {native_stats['max']:8.1f} | {native_stats['p50']:8.1f} | {native_stats['p95']:8.1f} | {native_stats['p99']:8.1f} | {native_stats['avg_file_count']:9.1f} | {native_stats['success_rate']:.0f}%"
        )

        print("\n\nCOMPARISON")
        print("----------")
        print(
            f"find-bash:   {bash_stats['avg']:.1f} ms (avg {bash_stats['avg_file_count']:.1f} files)"
        )
        print(f"fd:          {fd_stats['avg']:.1f} ms (avg {fd_stats['avg_file_count']:.1f} files)")
        print(
            f"native-find: {native_stats['avg']:.1f} ms (avg {native_stats['avg_file_count']:.1f} files)"
        )

        times = [
            {"method": "find-bash", "avg": bash_stats["avg"]},
            {"method": "fd", "avg": fd_stats["avg"]},
            {"method": "native-find", "avg": native_stats["avg"]},
        ]
        times.sort(key=lambda x: x["avg"])

        print(f"\nFastest: {times[0]['method']} ({times[0]['avg']:.1f} ms)")
        print(f"Slowest: {times[2]['method']} ({times[2]['avg']:.1f} ms)")
        print(f"Speedup (fastest vs slowest): {times[2]['avg'] / times[0]['avg']:.2f}x")

        print("\n========================================\n")

    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        import traceback

        traceback.print_exc()
        raise

    print(f"💾 Sandbox '{SANDBOX_NAME}' remains available.")


if __name__ == "__main__":
    asyncio.run(main())
