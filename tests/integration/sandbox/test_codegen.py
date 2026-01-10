import os

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
@pytest.mark.skipif("not os.environ.get('RELACE_API_KEY')", reason="RELACE_API_KEY not set")
class TestFastapplyWithRelace:
    """Test fastapply with Relace backend."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("codegen-relace")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "envs": [
                    {"name": "RELACE_API_KEY", "value": os.environ.get("RELACE_API_KEY", "")},
                ],
                "labels": default_labels,
            }
        )

        yield

        # Cleanup
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_applies_code_edit_to_create_new_file(self):
        """Test applying code edit to create a new file."""
        await self.sandbox.codegen.fastapply(
            "/tmp/test.txt",
            "// ... existing code ...\nconsole.log('Hello, world!');",
        )

        content = await self.sandbox.fs.read("/tmp/test.txt")
        assert "Hello, world!" in content

    async def test_preserves_existing_content_when_applying_edits(self):
        """Test preserving existing content when applying edits."""
        # First edit
        await self.sandbox.codegen.fastapply(
            "/tmp/preserve-test.txt",
            "// ... existing code ...\nconsole.log('First line');",
        )

        # Second edit - should preserve first line
        await self.sandbox.codegen.fastapply(
            "/tmp/preserve-test.txt",
            "// ... keep existing code\nconsole.log('Second line');",
        )

        content = await self.sandbox.fs.read("/tmp/preserve-test.txt")
        assert "Second line" in content

    async def test_performs_reranking_search(self):
        """Test performing reranking search."""
        # Create test file
        await self.sandbox.fs.write("/tmp/search-test.txt", "The meaning of life is 42")

        result = await self.sandbox.codegen.reranking(
            "/tmp",
            "What is the meaning of life?",
            0.01,
            1000,
            r".*\.txt$",
        )

        assert result is not None
        assert result.files is not None
        assert any(f.path and "search-test.txt" in f.path for f in result.files)


@pytest.mark.asyncio(loop_scope="class")
@pytest.mark.skipif("not os.environ.get('MORPH_API_KEY')", reason="MORPH_API_KEY not set")
class TestFastapplyWithMorph:
    """Test fastapply with Morph backend."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("codegen-morph")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "envs": [
                    {"name": "MORPH_API_KEY", "value": os.environ.get("MORPH_API_KEY", "")},
                ],
                "labels": default_labels,
            }
        )

        yield

        # Cleanup
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_applies_code_edit_with_morph_backend(self):
        """Test applying code edit with Morph backend."""
        await self.sandbox.codegen.fastapply(
            "/tmp/morph-test.txt",
            "// ... existing code ...\nconsole.log('Hello from Morph!');",
        )

        content = await self.sandbox.fs.read("/tmp/morph-test.txt")
        assert "Hello from Morph!" in content

    async def test_performs_reranking_with_morph(self):
        """Test performing reranking with Morph."""
        await self.sandbox.fs.write("/tmp/morph-search.txt", "The answer is always 42")

        result = await self.sandbox.codegen.reranking(
            "/tmp",
            "What is the answer?",
            0.01,
            1000000,
            r".*\.txt$",
        )

        assert result is not None
        assert result.files is not None


@pytest.mark.skipif(
    "os.environ.get('RELACE_API_KEY') or os.environ.get('MORPH_API_KEY')", reason="API keys are set"
)
class TestCodegenSkipped:
    """Tests that are skipped when no API keys are set."""

    def test_skips_codegen_tests_without_api_keys(self):
        """Test that codegen tests are skipped without API keys."""
        print("Codegen tests skipped - set RELACE_API_KEY or MORPH_API_KEY to run")
        assert True
