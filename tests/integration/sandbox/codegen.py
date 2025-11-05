import asyncio
import os
import sys

import dotenv

from blaxel.core.sandbox import SandboxInstance

dotenv.load_dotenv()

async def test_relace():
    """Test codegen with Relace provider."""
    print("[RELACE] Starting test...")

    sandbox = await SandboxInstance.create({
        "envs": [
            {"name": "RELACE_API_KEY", "value": os.environ.get("RELACE_API_KEY", "")},
        ]
    })
    print(f"[RELACE] ✓ Sandbox created: {sandbox.metadata.name}")

    try:
        print("[RELACE] Applying first code edit...")
        await sandbox.codegen.fastapply(
            "/tmp/test.txt",
            "// ... existing code ...\nconsole.log('Hello, world!');"
        )
        print("[RELACE] ✓ First edit applied successfully")

        content = await sandbox.fs.read("/tmp/test.txt")
        print(f"[RELACE] Content after first edit: {content}")
        assert "Hello, world!" in content, "First edit should contain 'Hello, world!'"
        print("[RELACE] ✓ First edit assertion passed")

        print("[RELACE] Applying second code edit...")
        await sandbox.codegen.fastapply(
            "/tmp/test.txt",
            "// ... keep existing code\nconsole.log('The meaning of life is 42');"
        )
        print("[RELACE] ✓ Second edit applied successfully")

        content = await sandbox.fs.read("/tmp/test.txt")
        print(f"[RELACE] Content after second edit: {content}")
        assert "The meaning of life is 42" in content, "Second edit should contain 'The meaning of life is 42'"
        assert "Hello, world!" in content, "Original content should be preserved"
        print("[RELACE] ✓ Second edit assertions passed")

        print("[RELACE] Testing reranking...")
        result = await sandbox.codegen.reranking(
            "/tmp",
            "What is the meaning of life?",
            score_threshold=0.01,
            token_limit=1000,
            file_pattern=".*\\.txt$"
        )
        print(f"[RELACE] Reranking result: {result}")
        assert result is not None, "Reranking should return a result"
        assert any(f.path and "test.txt" in f.path for f in result.files), "Reranking should return the test.txt file"
        print("[RELACE] ✓ Reranking assertions passed")

        print("[RELACE] ✅ Test completed successfully")

    finally:
        await SandboxInstance.delete(sandbox.metadata.name)
        print("[RELACE] ✓ Sandbox cleaned up")


async def test_morph():
    """Test codegen with Morph provider."""
    print("[MORPH] Starting test...")

    sandbox = await SandboxInstance.create({
        "envs": [
            {"name": "MORPH_API_KEY", "value": os.environ.get("MORPH_API_KEY", "")},
        ]
    })
    print(f"[MORPH] ✓ Sandbox created: {sandbox.metadata.name}")

    try:
        print("[MORPH] Applying first code edit...")
        await sandbox.codegen.fastapply(
            "/tmp/test.txt",
            "// ... existing code ...\nconsole.log('Hello, world!');"
        )
        print("[MORPH] ✓ First edit applied successfully")

        content = await sandbox.fs.read("/tmp/test.txt")
        print(f"[MORPH] Content after first edit: {content}")
        assert "Hello, world!" in content, "First edit should contain 'Hello, world!'"
        print("[MORPH] ✓ First edit assertion passed")

        print("[MORPH] Applying second code edit...")
        await sandbox.codegen.fastapply(
            "/tmp/test.txt",
            "// ... keep existing code\nconsole.log('The meaning of life is 42');"
        )
        print("[MORPH] ✓ Second edit applied successfully")

        content = await sandbox.fs.read("/tmp/test.txt")
        print(f"[MORPH] Content after second edit: {content}")
        assert "The meaning of life is 42" in content, "Second edit should contain 'The meaning of life is 42'"
        assert "Hello, world!" in content, "Original content should be preserved"
        print("[MORPH] ✓ Second edit assertions passed")

        print("[MORPH] Testing reranking...")
        result = await sandbox.codegen.reranking(
            "/tmp",
            "What is the meaning of life?",
            score_threshold=0.01,
            token_limit=1000000,
            file_pattern=".*\\.txt$"
        )
        print(f"[MORPH] Reranking result: {result}")
        assert result is not None, "Reranking should return a result"
        assert any(f.path and "test.txt" in f.path for f in result.files), "Reranking should return the test.txt file"
        print("[MORPH] ✓ Reranking assertions passed")

        print("[MORPH] ✅ Test completed successfully")

    finally:
        await SandboxInstance.delete(sandbox.metadata.name)
        print("[MORPH] ✓ Sandbox cleaned up")


async def main():
    """Run all codegen tests."""
    print("=== Starting Codegen Tests ===\n")

    try:
        await test_relace()
        print("\n")
        await test_morph()
        print("\n✅ === All tests passed! ===")
    except Exception as error:
        print("\n❌ === Test failed with error ===")
        print(error)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

