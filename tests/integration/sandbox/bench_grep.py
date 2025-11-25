import asyncio
import statistics
import time
from typing import Any, Dict, List

from blaxel.core.sandbox import SandboxInstance

# ============ CONFIGURATION ============
ITERATIONS_PER_TEST = 20
WARMUP_ITERATIONS = 3
SANDBOX_NAME = "fzf-test"
REPO_URL = "https://github.com/relace-ai/vite-template.git"
REPO_PATH = "/workspace/vite-grep"
SEARCH_TERM = "script"
SETUP_ENVIRONMENT = True
# =======================================


async def bench_grep_bash(sandbox: SandboxInstance) -> Dict[str, Any]:
    """Benchmark bash grep command."""
    start = time.time()
    
    result = await sandbox.process.exec({
        "command": f'grep -r "{SEARCH_TERM}" {REPO_PATH} 2>/dev/null | head -100',
        "waitForCompletion": True,
    })
    
    duration = (time.time() - start) * 1000  # Convert to ms
    output = result.logs or ""
    lines = [line for line in output.strip().split('\n') if line]
    match_count = len(lines)
    
    return {
        'method': 'grep-bash',
        'duration': duration,
        'match_count': match_count,
        'success': True
    }


async def bench_ripgrep(sandbox: SandboxInstance) -> Dict[str, Any]:
    """Benchmark ripgrep command."""
    start = time.time()
    
    result = await sandbox.process.exec({
        "command": f'rg "{SEARCH_TERM}" {REPO_PATH} | head -100',
        "waitForCompletion": True,
    })
    
    duration = (time.time() - start) * 1000  # Convert to ms
    output = result.logs or ""
    lines = [line for line in output.strip().split('\n') if line]
    match_count = len(lines)
    
    return {
        'method': 'ripgrep',
        'duration': duration,
        'match_count': match_count,
        'success': True
    }


async def bench_native_grep(sandbox: SandboxInstance) -> Dict[str, Any]:
    """Benchmark native grep method."""
    start = time.time()
    
    result = await sandbox.fs.grep(
        query=SEARCH_TERM,
        path=REPO_PATH,
        max_results=100,
    )
    
    duration = (time.time() - start) * 1000  # Convert to ms
    match_count = len(result.matches) if result.matches else 0
    
    return {
        'method': 'native-grep',
        'duration': duration,
        'match_count': match_count,
        'success': True
    }


async def setup_environment(sandbox: SandboxInstance) -> None:
    """Setup test environment."""
    print("📦 Setting up environment...")
    
    print("   Installing ripgrep...")
    await sandbox.process.exec({
        "command": "apk add ripgrep",
        "waitForCompletion": True,
    })
    
    print(f"   Cloning {REPO_URL}...")
    await sandbox.process.exec({
        "command": f"git clone {REPO_URL} {REPO_PATH}",
        "waitForCompletion": True,
    })
    
    print("✓ Environment ready")


def calculate_stats(results: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate statistics from benchmark results."""
    durations = [r['duration'] for r in results if r['success']]
    match_counts = [r['match_count'] for r in results if r['success']]
    
    durations_sorted = sorted(durations)
    
    return {
        'avg': statistics.mean(durations) if durations else 0,
        'min': min(durations) if durations else 0,
        'max': max(durations) if durations else 0,
        'p50': durations_sorted[len(durations_sorted) // 2] if durations_sorted else 0,
        'p95': durations_sorted[int(len(durations_sorted) * 0.95)] if durations_sorted else 0,
        'p99': durations_sorted[int(len(durations_sorted) * 0.99)] if durations_sorted else 0,
        'avg_match_count': statistics.mean(match_counts) if match_counts else 0,
        'success_rate': (len([r for r in results if r['success']]) / len(results)) * 100 if results else 0,
    }


async def main():
    """Main benchmark function."""
    print("========================================")
    print("  GREP BENCHMARK (Python SDK)")
    print("========================================")
    print("\n⚙️  Configuration:")
    print(f"   Sandbox: {SANDBOX_NAME}")
    print(f"   Repository: {REPO_URL}")
    print(f"   Path: {REPO_PATH}")
    print(f"   Search term: \"{SEARCH_TERM}\"")
    print(f"   Iterations: {ITERATIONS_PER_TEST}\n")

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
        print("🔍 Validation...")
        
        bash_val = await sandbox.process.exec({
            "command": f'grep -r "{SEARCH_TERM}" {REPO_PATH} 2>/dev/null | head -10',
            "waitForCompletion": True,
        })
        bash_lines = [line for line in (bash_val.logs or "").strip().split('\n') if line]
        print(f"   grep-bash:   {len(bash_lines)} matches")
        for line in bash_lines[:2]:
            print(f"                - {line[:80]}")
        
        rg_val = await sandbox.process.exec({
            "command": f'rg "{SEARCH_TERM}" {REPO_PATH} | head -10',
            "waitForCompletion": True,
        })
        rg_lines = [line for line in (rg_val.logs or "").strip().split('\n') if line]
        print(f"   ripgrep:     {len(rg_lines)} matches")
        for line in rg_lines[:2]:
            print(f"                - {line[:80]}")
        
        native_val = await sandbox.fs.grep(
            query=SEARCH_TERM,
            path=REPO_PATH,
            max_results=10,
        )
        print(f"   native:      {len(native_val.matches) if native_val.matches else 0} matches")
        if native_val.matches:
            for m in native_val.matches[:2]:
                text = m.text[:60] if m.text else ""
                print(f"                - {m.path}:{m.line}: {text}")

        all_results: List[Dict[str, Any]] = []

        # Warmup
        print(f"\n🔥 Warmup ({WARMUP_ITERATIONS} iterations)...")
        for i in range(WARMUP_ITERATIONS):
            await bench_grep_bash(sandbox)
            await bench_ripgrep(sandbox)
            await bench_native_grep(sandbox)
        print("✓ Warmup complete")

        # Benchmark grep-bash
        print(f"\n📊 Benchmarking grep-bash ({ITERATIONS_PER_TEST} iterations)...")
        for i in range(ITERATIONS_PER_TEST):
            result = await bench_grep_bash(sandbox)
            all_results.append(result)
            if (i + 1) % 5 == 0:
                print(f"   Progress: {i + 1}/{ITERATIONS_PER_TEST}")

        # Benchmark ripgrep
        print(f"\n📊 Benchmarking ripgrep ({ITERATIONS_PER_TEST} iterations)...")
        for i in range(ITERATIONS_PER_TEST):
            result = await bench_ripgrep(sandbox)
            all_results.append(result)
            if (i + 1) % 5 == 0:
                print(f"   Progress: {i + 1}/{ITERATIONS_PER_TEST}")

        # Benchmark native-grep
        print(f"\n📊 Benchmarking native-grep ({ITERATIONS_PER_TEST} iterations)...")
        for i in range(ITERATIONS_PER_TEST):
            result = await bench_native_grep(sandbox)
            all_results.append(result)
            if (i + 1) % 5 == 0:
                print(f"   Progress: {i + 1}/{ITERATIONS_PER_TEST}")

        # Calculate statistics
        bash_results = [r for r in all_results if r['method'] == 'grep-bash']
        rg_results = [r for r in all_results if r['method'] == 'ripgrep']
        native_results = [r for r in all_results if r['method'] == 'native-grep']

        bash_stats = calculate_stats(bash_results)
        rg_stats = calculate_stats(rg_results)
        native_stats = calculate_stats(native_results)

        # Display results
        print("\n\n========================================")
        print("           RESULTS")
        print("========================================\n")

        print("Method        | Avg (ms) | Min (ms) | Max (ms) | P50 (ms) | P95 (ms) | P99 (ms) | Avg Matches | Success")
        print("--------------|----------|----------|----------|----------|----------|----------|-------------|--------")

        print(f"grep-bash     | {bash_stats['avg']:8.1f} | {bash_stats['min']:8.1f} | {bash_stats['max']:8.1f} | {bash_stats['p50']:8.1f} | {bash_stats['p95']:8.1f} | {bash_stats['p99']:8.1f} | {bash_stats['avg_match_count']:11.1f} | {bash_stats['success_rate']:.0f}%")
        print(f"ripgrep       | {rg_stats['avg']:8.1f} | {rg_stats['min']:8.1f} | {rg_stats['max']:8.1f} | {rg_stats['p50']:8.1f} | {rg_stats['p95']:8.1f} | {rg_stats['p99']:8.1f} | {rg_stats['avg_match_count']:11.1f} | {rg_stats['success_rate']:.0f}%")
        print(f"native-grep   | {native_stats['avg']:8.1f} | {native_stats['min']:8.1f} | {native_stats['max']:8.1f} | {native_stats['p50']:8.1f} | {native_stats['p95']:8.1f} | {native_stats['p99']:8.1f} | {native_stats['avg_match_count']:11.1f} | {native_stats['success_rate']:.0f}%")

        print("\n\nCOMPARISON")
        print("----------")
        print(f"grep-bash:   {bash_stats['avg']:.1f} ms (avg {bash_stats['avg_match_count']:.1f} matches)")
        print(f"ripgrep:     {rg_stats['avg']:.1f} ms (avg {rg_stats['avg_match_count']:.1f} matches)")
        print(f"native-grep: {native_stats['avg']:.1f} ms (avg {native_stats['avg_match_count']:.1f} matches)")
        
        times = [
            {'method': 'grep-bash', 'avg': bash_stats['avg']},
            {'method': 'ripgrep', 'avg': rg_stats['avg']},
            {'method': 'native-grep', 'avg': native_stats['avg']},
        ]
        times.sort(key=lambda x: x['avg'])
        
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

