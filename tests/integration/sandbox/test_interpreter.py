import pytest
import pytest_asyncio

from blaxel.core.sandbox import CodeInterpreter
from tests.helpers import default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestCodeInterpreterOperations:
    """Test CodeInterpreter operations."""

    interpreter: CodeInterpreter = None
    interpreter_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_interpreter(self, request):
        """Set up a code interpreter for the test class."""
        request.cls.interpreter_name = unique_name("interp")
        request.cls.interpreter = await CodeInterpreter.create(
            {
                "name": request.cls.interpreter_name,
                "labels": default_labels,
            }
        )

        yield

        # Cleanup
        if request.cls.interpreter and request.cls.interpreter.metadata:
            try:
                await CodeInterpreter.delete(request.cls.interpreter.metadata.name)
            except Exception:
                pass


@pytest.mark.asyncio(loop_scope="class")
class TestCodeInterpreterCreate(TestCodeInterpreterOperations):
    """Test interpreter creation."""

    async def test_creates_code_interpreter(self):
        """Test that a code interpreter is created."""
        assert self.interpreter.metadata is not None
        assert self.interpreter.metadata.name is not None


@pytest.mark.asyncio(loop_scope="class")
class TestCodeInterpreterContext(TestCodeInterpreterOperations):
    """Test code context creation."""

    async def test_creates_python_code_context(self):
        """Test creating a Python code context."""
        ctx = await self.interpreter.create_code_context(language="python")

        assert ctx is not None
        assert ctx.id is not None


@pytest.mark.asyncio(loop_scope="class")
class TestRunCode(TestCodeInterpreterOperations):
    """Test runCode operations."""

    async def test_executes_simple_python_code(self):
        """Test executing simple Python code."""
        stdout_lines = []

        await self.interpreter.run_code(
            "print('Hello from interpreter')",
            language="python",
            on_stdout=lambda msg: stdout_lines.append(msg.text),
            timeout=30.0,
        )

        assert "Hello from interpreter" in "".join(stdout_lines)

    async def test_captures_stderr_output(self):
        """Test capturing stderr output."""
        stderr_lines = []

        await self.interpreter.run_code(
            "import sys; sys.stderr.write('error message')",
            language="python",
            on_stderr=lambda msg: stderr_lines.append(msg.text),
            timeout=30.0,
        )

        assert "error message" in "".join(stderr_lines)

    async def test_returns_execution_results(self):
        """Test returning execution results."""
        results = []

        await self.interpreter.run_code(
            "2 + 2",
            language="python",
            on_result=lambda res: results.append(res),
            timeout=30.0,
        )

        assert len(results) > 0

    async def test_captures_execution_errors(self):
        """Test capturing execution errors."""
        errors = []

        await self.interpreter.run_code(
            "raise ValueError('test error')",
            language="python",
            on_error=lambda err: errors.append(err),
            timeout=30.0,
        )

        assert len(errors) > 0
        assert errors[0].name == "ValueError"

    async def test_persists_state_across_runs(self):
        """Test that state persists across runs."""
        # Define a function in first run
        await self.interpreter.run_code(
            "def add(a, b):\n    return a + b",
            language="python",
            timeout=30.0,
        )

        # Call the function in second run
        stdout_lines = []
        await self.interpreter.run_code(
            "print(add(2, 3))",
            language="python",
            on_stdout=lambda msg: stdout_lines.append(msg.text),
            timeout=30.0,
        )

        assert "5" in "".join(stdout_lines)

    async def test_handles_variables_across_runs(self):
        """Test handling variables across runs."""
        # Set variable
        await self.interpreter.run_code(
            "x = 42",
            language="python",
            timeout=30.0,
        )

        # Read variable
        stdout_lines = []
        await self.interpreter.run_code(
            "print(x)",
            language="python",
            on_stdout=lambda msg: stdout_lines.append(msg.text),
            timeout=30.0,
        )

        assert "42" in "".join(stdout_lines)


@pytest.mark.asyncio(loop_scope="class")
class TestCodeInterpreterStaticMethods(TestCodeInterpreterOperations):
    """Test static methods."""

    async def test_gets_existing_interpreter(self):
        """Test getting an existing interpreter."""
        retrieved = await CodeInterpreter.get(self.interpreter.metadata.name)

        assert retrieved.metadata.name == self.interpreter.metadata.name
