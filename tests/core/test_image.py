"""Tests for Image builder functionality."""

import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest

from blaxel.core.image import ImageBuildContext, ImageInstance, LocalFile


@pytest.fixture
def temp_dir():
    """Create a temporary directory that is cleaned up after the test."""
    tmpdir = tempfile.mkdtemp(prefix="blaxel-test-")
    yield Path(tmpdir)
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def temp_file():
    """Create a temporary file that is cleaned up after the test."""
    fd, path = tempfile.mkstemp(suffix=".txt", prefix="blaxel-test-")
    os.write(fd, b"test content")
    os.close(fd)
    yield Path(path)
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def temp_source_dir():
    """Create a temporary directory with test files that is cleaned up after the test."""
    tmpdir = tempfile.mkdtemp(prefix="blaxel-source-")
    source_path = Path(tmpdir)
    (source_path / "file1.txt").write_text("content1")
    (source_path / "file2.txt").write_text("content2")
    (source_path / "subdir").mkdir()
    (source_path / "subdir" / "nested.txt").write_text("nested content")
    yield source_path
    shutil.rmtree(tmpdir, ignore_errors=True)


class TestImageFromRegistry:
    """Tests for ImageInstance.from_registry()."""

    def test_from_registry_creates_image(self):
        """Test that from_registry creates an Image with the correct base image."""
        image = ImageInstance.from_registry("python:3.11-slim")
        assert image.base_image == "python:3.11-slim"

    def test_from_registry_with_dockerhub_image(self):
        """Test from_registry with a full DockerHub image tag."""
        image = ImageInstance.from_registry(
            "namanjain12/numpy_final:05aa44d53f4f9528847a0c014fe4bda5caa5fd3d"
        )
        assert (
            image.base_image
            == "namanjain12/numpy_final:05aa44d53f4f9528847a0c014fe4bda5caa5fd3d"
        )

    def test_from_registry_dockerfile_content(self):
        """Test that the generated Dockerfile has correct FROM instruction."""
        image = ImageInstance.from_registry("ubuntu:22.04")
        assert "FROM ubuntu:22.04" in image.dockerfile

    def test_from_registry_with_private_registry(self):
        """Test from_registry with a private registry URL."""
        image = ImageInstance.from_registry("gcr.io/my-project/my-image:v1.0.0")
        assert image.base_image == "gcr.io/my-project/my-image:v1.0.0"
        assert "FROM gcr.io/my-project/my-image:v1.0.0" in image.dockerfile

    def test_from_registry_with_digest(self):
        """Test from_registry with image digest instead of tag."""
        image = ImageInstance.from_registry(
            "python@sha256:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
        )
        assert "sha256:abcdef" in image.base_image


class TestImageWorkdir:
    """Tests for ImageInstance.workdir()."""

    def test_workdir_adds_instruction(self):
        """Test that workdir adds WORKDIR instruction."""
        image = ImageInstance.from_registry("python:3.11").workdir("/app")
        assert "WORKDIR /app" in image.dockerfile

    def test_workdir_returns_new_image(self):
        """Test that workdir returns a new Image instance (immutability)."""
        image1 = ImageInstance.from_registry("python:3.11")
        image2 = image1.workdir("/app")
        assert image1 is not image2
        assert "WORKDIR /app" not in image1.dockerfile
        assert "WORKDIR /app" in image2.dockerfile

    def test_workdir_multiple_changes(self):
        """Test multiple workdir changes in sequence."""
        image = (
            ImageInstance.from_registry("python:3.11")
            .workdir("/first")
            .run_commands("echo first")
            .workdir("/second")
            .run_commands("echo second")
        )
        dockerfile = image.dockerfile
        assert "WORKDIR /first" in dockerfile
        assert "WORKDIR /second" in dockerfile
        # Check order
        first_idx = dockerfile.index("WORKDIR /first")
        second_idx = dockerfile.index("WORKDIR /second")
        assert first_idx < second_idx


class TestImageRunCommands:
    """Tests for ImageInstance.run_commands()."""

    def test_run_commands_single(self):
        """Test run_commands with a single command."""
        image = ImageInstance.from_registry("python:3.11").run_commands("echo hello")
        assert "RUN echo hello" in image.dockerfile

    def test_run_commands_multiple(self):
        """Test run_commands with multiple commands."""
        image = ImageInstance.from_registry("python:3.11").run_commands(
            "echo hello",
            "echo world",
        )
        assert "RUN echo hello" in image.dockerfile
        assert "RUN echo world" in image.dockerfile

    def test_run_commands_chained(self):
        """Test chaining multiple run_commands calls."""
        image = (
            ImageInstance.from_registry("python:3.11")
            .run_commands("echo first")
            .run_commands("echo second")
        )
        assert "RUN echo first" in image.dockerfile
        assert "RUN echo second" in image.dockerfile

    def test_run_commands_with_complex_shell(self):
        """Test run_commands with complex shell commands."""
        image = ImageInstance.from_registry("python:3.11").run_commands(
            "cd /app && git clone https://github.com/example/repo.git",
            "find . -name '*.pyc' -delete",
            "chmod +x ./run_tests.sh && ./run_tests.sh",
        )
        dockerfile = image.dockerfile
        assert "git clone" in dockerfile
        assert "find . -name" in dockerfile
        assert "chmod +x" in dockerfile

    def test_run_commands_with_multiline_heredoc(self):
        """Test run_commands with heredoc-style content."""
        image = ImageInstance.from_registry("python:3.11").run_commands(
            "cat > /app/config.json << 'EOF'\n{\"key\": \"value\"}\nEOF"
        )
        assert "cat > /app/config.json" in image.dockerfile


class TestImageEnv:
    """Tests for ImageInstance.env()."""

    def test_env_single_variable(self):
        """Test env with a single variable."""
        image = ImageInstance.from_registry("python:3.11").env(PYTHONUNBUFFERED="1")
        assert 'ENV PYTHONUNBUFFERED="1"' in image.dockerfile

    def test_env_multiple_variables(self):
        """Test env with multiple variables."""
        image = ImageInstance.from_registry("python:3.11").env(
            PYTHONUNBUFFERED="1",
            DEBUG="true",
        )
        assert 'ENV PYTHONUNBUFFERED="1"' in image.dockerfile
        assert 'ENV DEBUG="true"' in image.dockerfile

    def test_env_empty_returns_same_image(self):
        """Test that env with no variables returns the same image."""
        image1 = ImageInstance.from_registry("python:3.11")
        image2 = image1.env()
        assert image1 is image2

    def test_env_with_special_characters(self):
        """Test env with special characters in values."""
        image = ImageInstance.from_registry("python:3.11").env(
            PATH="/usr/local/bin:$PATH",
            CONNECTION_STRING="host=localhost;port=5432",
        )
        dockerfile = image.dockerfile
        assert 'ENV PATH="/usr/local/bin:$PATH"' in dockerfile
        assert 'ENV CONNECTION_STRING="host=localhost;port=5432"' in dockerfile


class TestImageCopy:
    """Tests for ImageInstance.copy()."""

    def test_copy_instruction(self):
        """Test copy adds COPY instruction."""
        image = ImageInstance.from_registry("python:3.11").copy(".", "/app")
        assert "COPY . /app" in image.dockerfile

    def test_copy_with_chown(self):
        """Test copy with specific paths."""
        image = ImageInstance.from_registry("python:3.11").copy(
            "requirements.txt", "/app/requirements.txt"
        )
        assert "COPY requirements.txt /app/requirements.txt" in image.dockerfile

    def test_copy_multiple(self):
        """Test multiple copy instructions."""
        image = (
            ImageInstance.from_registry("python:3.11")
            .copy("requirements.txt", "/app/requirements.txt")
            .copy("src/", "/app/src/")
        )
        dockerfile = image.dockerfile
        assert "COPY requirements.txt /app/requirements.txt" in dockerfile
        assert "COPY src/ /app/src/" in dockerfile


class TestImageExpose:
    """Tests for ImageInstance.expose()."""

    def test_expose_single_port(self):
        """Test expose with a single port."""
        image = ImageInstance.from_registry("python:3.11").expose(8080)
        assert "EXPOSE 8080" in image.dockerfile

    def test_expose_multiple_ports(self):
        """Test expose with multiple ports."""
        image = ImageInstance.from_registry("python:3.11").expose(80, 443, 8080)
        assert "EXPOSE 80" in image.dockerfile
        assert "EXPOSE 443" in image.dockerfile
        assert "EXPOSE 8080" in image.dockerfile

    def test_expose_empty_returns_same_image(self):
        """Test that expose with no ports returns the same image."""
        image1 = ImageInstance.from_registry("python:3.11")
        image2 = image1.expose()
        assert image1 is image2


class TestImageEntrypoint:
    """Tests for ImageInstance.entrypoint()."""

    def test_entrypoint_single_arg(self):
        """Test entrypoint with a single argument."""
        image = ImageInstance.from_registry("python:3.11").entrypoint("python")
        assert 'ENTRYPOINT ["python"]' in image.dockerfile

    def test_entrypoint_multiple_args(self):
        """Test entrypoint with multiple arguments."""
        image = ImageInstance.from_registry("python:3.11").entrypoint("python", "-m", "app")
        assert 'ENTRYPOINT ["python", "-m", "app"]' in image.dockerfile

    def test_entrypoint_empty_returns_same_image(self):
        """Test that entrypoint with no args returns the same image."""
        image1 = ImageInstance.from_registry("python:3.11")
        image2 = image1.entrypoint()
        assert image1 is image2


class TestImageUser:
    """Tests for ImageInstance.user()."""

    def test_user_by_name(self):
        """Test user with username."""
        image = ImageInstance.from_registry("python:3.11").user("appuser")
        assert "USER appuser" in image.dockerfile

    def test_user_by_uid(self):
        """Test user with UID."""
        image = ImageInstance.from_registry("python:3.11").user("1000")
        assert "USER 1000" in image.dockerfile

    def test_user_with_group(self):
        """Test user with UID:GID format."""
        image = ImageInstance.from_registry("python:3.11").user("1000:1000")
        assert "USER 1000:1000" in image.dockerfile


class TestImageLabel:
    """Tests for ImageInstance.label()."""

    def test_label_single(self):
        """Test label with single label."""
        image = ImageInstance.from_registry("python:3.11").label(version="1.0")
        assert 'LABEL version="1.0"' in image.dockerfile

    def test_label_multiple(self):
        """Test label with multiple labels."""
        image = ImageInstance.from_registry("python:3.11").label(
            version="1.0",
            maintainer="test@example.com",
        )
        assert 'LABEL version="1.0"' in image.dockerfile
        assert 'LABEL maintainer="test@example.com"' in image.dockerfile

    def test_label_empty_returns_same_image(self):
        """Test that label with no labels returns the same image."""
        image1 = ImageInstance.from_registry("python:3.11")
        image2 = image1.label()
        assert image1 is image2


class TestImageArg:
    """Tests for ImageInstance.arg()."""

    def test_arg_without_default(self):
        """Test arg without default value."""
        image = ImageInstance.from_registry("python:3.11").arg("VERSION")
        assert "ARG VERSION" in image.dockerfile

    def test_arg_with_default(self):
        """Test arg with default value."""
        image = ImageInstance.from_registry("python:3.11").arg("VERSION", "1.0")
        assert "ARG VERSION=1.0" in image.dockerfile

    def test_arg_multiple(self):
        """Test multiple ARG instructions."""
        image = (
            ImageInstance.from_registry("python:3.11")
            .arg("VERSION", "1.0")
            .arg("BUILD_DATE")
            .arg("GIT_COMMIT", "unknown")
        )
        dockerfile = image.dockerfile
        assert "ARG VERSION=1.0" in dockerfile
        assert "ARG BUILD_DATE" in dockerfile
        assert "ARG GIT_COMMIT=unknown" in dockerfile


class TestImageChaining:
    """Tests for fluent API chaining."""

    def test_full_chain(self):
        """Test a complete chain of operations."""
        image = (
            ImageInstance.from_registry("python:3.11-slim")
            .run_commands("apt-get update && apt-get install -y git curl")
            .workdir("/app")
            .copy(".", "/app")
            .run_commands("pip install -r requirements.txt")
            .env(PYTHONUNBUFFERED="1")
            .expose(8080)
        )

        dockerfile = image.dockerfile
        assert "FROM python:3.11-slim" in dockerfile
        assert "apt-get install" in dockerfile
        assert "WORKDIR /app" in dockerfile
        assert "COPY . /app" in dockerfile
        assert "RUN pip install -r requirements.txt" in dockerfile
        assert 'ENV PYTHONUNBUFFERED="1"' in dockerfile
        assert "EXPOSE 8080" in dockerfile

    def test_immutability(self):
        """Test that chaining creates new instances (immutability)."""
        base = ImageInstance.from_registry("python:3.11")
        with_workdir = base.workdir("/app")
        with_env = with_workdir.env(DEBUG="true")

        # Each should be a different instance
        assert base is not with_workdir
        assert with_workdir is not with_env
        assert base is not with_env

        # Original should not be modified
        assert "WORKDIR" not in base.dockerfile
        assert "ENV" not in base.dockerfile

    def test_r2e_eval_harness_pattern(self):
        """Test the R2E eval harness pattern from the issue."""
        image = (
            ImageInstance.from_registry(
                "namanjain12/numpy_final:05aa44d53f4f9528847a0c014fe4bda5caa5fd3d"
            )
            .workdir("/testbed")
            .run_commands("chmod +x ./run_tests.sh")
            .run_commands("ln -s /r2e_tests /testbed/r2e_tests")
            .run_commands("apt-get update && apt-get install -y git git-lfs ripgrep")
            .run_commands(
                "git config --global user.name 'Relace'",
                "git config --global user.email 'noreply@relace.ai'",
                "git lfs install",
            )
        )

        dockerfile = image.dockerfile
        assert "FROM namanjain12/numpy_final:" in dockerfile
        assert "WORKDIR /testbed" in dockerfile
        assert "chmod +x ./run_tests.sh" in dockerfile
        assert "ln -s /r2e_tests" in dockerfile
        assert "git git-lfs ripgrep" in dockerfile
        assert "git config --global user.name" in dockerfile

    def test_complex_web_app_image(self):
        """Test building a complex web application image."""
        image = (
            ImageInstance.from_registry("python:3.11-slim")
            .arg("APP_VERSION", "1.0.0")
            .label(
                maintainer="dev@example.com",
                version="1.0.0",
            )
            .run_commands("apt-get update && apt-get install -y curl ca-certificates")
            .workdir("/app")
            .env(
                PYTHONUNBUFFERED="1",
                PYTHONDONTWRITEBYTECODE="1",
                PIP_NO_CACHE_DIR="1",
            )
            .copy("requirements.txt", "/app/requirements.txt")
            .run_commands("pip install -r requirements.txt")
            .copy(".", "/app")
            .user("1000:1000")
            .expose(8000)
            .entrypoint("python", "-m", "gunicorn")
        )

        dockerfile = image.dockerfile
        assert "FROM python:3.11-slim" in dockerfile
        assert "ARG APP_VERSION=1.0.0" in dockerfile
        assert 'LABEL maintainer="dev@example.com"' in dockerfile
        assert "apt-get install" in dockerfile
        assert "WORKDIR /app" in dockerfile
        assert "PYTHONUNBUFFERED" in dockerfile
        assert "USER 1000:1000" in dockerfile
        assert "EXPOSE 8000" in dockerfile
        assert "ENTRYPOINT" in dockerfile


class TestImageHash:
    """Tests for ImageInstance.hash property."""

    def test_hash_consistency(self):
        """Test that same image produces same hash."""
        image1 = ImageInstance.from_registry("python:3.11").workdir("/app")
        image2 = ImageInstance.from_registry("python:3.11").workdir("/app")
        assert image1.hash == image2.hash

    def test_hash_different_for_different_images(self):
        """Test that different images produce different hashes."""
        image1 = ImageInstance.from_registry("python:3.11").workdir("/app")
        image2 = ImageInstance.from_registry("python:3.11").workdir("/other")
        assert image1.hash != image2.hash

    def test_hash_different_for_different_base_images(self):
        """Test that different base images produce different hashes."""
        image1 = ImageInstance.from_registry("python:3.11").workdir("/app")
        image2 = ImageInstance.from_registry("python:3.12").workdir("/app")
        assert image1.hash != image2.hash

    def test_hash_length(self):
        """Test hash length is consistent."""
        image = ImageInstance.from_registry("python:3.11").workdir("/app")
        assert len(image.hash) == 12


class TestImageWrite:
    """Tests for ImageInstance.write() method."""

    def test_write_creates_dockerfile(self, temp_dir):
        """Test that build creates a Dockerfile."""
        image = ImageInstance.from_registry("python:3.11").workdir("/app")
        build_dir = image.write(str(temp_dir), name="test-image")
        dockerfile_path = build_dir / "Dockerfile"

        assert dockerfile_path.exists()
        content = dockerfile_path.read_text()
        assert "FROM python:3.11" in content
        assert "WORKDIR /app" in content

    def test_write_creates_manifest(self, temp_dir):
        """Test that build creates a manifest.json."""
        image = ImageInstance.from_registry("python:3.11").workdir("/app")
        build_dir = image.write(str(temp_dir), name="test-image")
        manifest_path = build_dir / "manifest.json"

        assert manifest_path.exists()
        manifest = json.loads(manifest_path.read_text())
        assert manifest["base_image"] == "python:3.11"
        assert "hash" in manifest
        assert manifest["instructions_count"] == 1

    def test_write_with_auto_name(self, temp_dir):
        """Test that build auto-generates folder name from hash."""
        image = ImageInstance.from_registry("python:3.11")
        build_dir = image.write(str(temp_dir))
        assert build_dir.name.startswith("image-")
        assert len(build_dir.name) == 6 + 12  # "image-" + 12 char hash

    def test_write_temp(self):
        """Test build_temp creates in temporary directory."""
        image = ImageInstance.from_registry("python:3.11").workdir("/app")
        build_dir = None
        try:
            build_dir = image.write_temp()
            assert build_dir.exists()
            assert (build_dir / "Dockerfile").exists()
            assert (build_dir / "manifest.json").exists()
        finally:
            if build_dir:
                shutil.rmtree(build_dir.parent, ignore_errors=True)

    def test_write_overwrites_existing(self, temp_dir):
        """Test that build overwrites existing directory."""
        image1 = ImageInstance.from_registry("python:3.11").workdir("/app")
        image2 = ImageInstance.from_registry("python:3.12").workdir("/other")

        build_dir1 = image1.write(str(temp_dir), name="test-image")
        build_dir2 = image2.write(str(temp_dir), name="test-image")

        assert build_dir1 == build_dir2
        content = (build_dir2 / "Dockerfile").read_text()
        assert "FROM python:3.12" in content
        assert "WORKDIR /other" in content

    def test_write_creates_nested_directories(self, temp_dir):
        """Test that build creates nested directories if needed."""
        image = ImageInstance.from_registry("python:3.11")
        nested_path = temp_dir / "deep" / "nested" / "path"
        build_dir = image.write(str(nested_path), name="test-image")

        assert build_dir.exists()
        assert (build_dir / "Dockerfile").exists()

    def test_write_manifest_contains_correct_counts(self, temp_dir, temp_file):
        """Test that manifest contains correct instruction and file counts."""
        image = (
            ImageInstance.from_registry("python:3.11")
            .workdir("/app")
            .run_commands("echo hello", "echo world")
            .add_local_file(str(temp_file), "/app/file.txt")
        )
        build_dir = image.write(str(temp_dir), name="test-image")
        manifest = json.loads((build_dir / "manifest.json").read_text())

        assert manifest["instructions_count"] == 4  # WORKDIR + 2 RUN + COPY
        assert manifest["local_files_count"] == 1


class TestImageAddLocalFile:
    """Tests for ImageInstance.add_local_file() method."""

    def test_add_local_file_instruction(self, temp_file):
        """Test that add_local_file adds COPY instruction."""
        image = ImageInstance.from_registry("python:3.11").add_local_file(
            str(temp_file), "/app/file.txt"
        )
        assert "COPY" in image.dockerfile

    def test_add_local_file_copies_to_build_context(self, temp_file, temp_dir):
        """Test that add_local_file copies file to build context."""
        image = ImageInstance.from_registry("python:3.11").add_local_file(
            str(temp_file), "/app/file.txt", context_name="myfile.txt"
        )
        build_dir = image.write(str(temp_dir), name="test-image")
        copied_file = build_dir / "myfile.txt"

        assert copied_file.exists()
        assert copied_file.read_text() == "test content"

    def test_add_local_file_missing_raises_error(self, temp_dir):
        """Test that add_local_file raises error for missing file."""
        image = ImageInstance.from_registry("python:3.11").add_local_file(
            "/nonexistent/file.txt", "/app/file.txt"
        )
        with pytest.raises(FileNotFoundError):
            image.write(str(temp_dir), name="test-image")

    def test_add_local_file_uses_filename_as_context_name(self, temp_file, temp_dir):
        """Test that add_local_file uses filename as default context name."""
        image = ImageInstance.from_registry("python:3.11").add_local_file(
            str(temp_file), "/app/file.txt"
        )
        build_dir = image.write(str(temp_dir), name="test-image")

        # Should use the temp file's name
        assert any(f.suffix == ".txt" for f in build_dir.iterdir())

    def test_add_multiple_local_files(self, temp_dir):
        """Test adding multiple local files."""
        file1 = temp_dir / "file1.txt"
        file2 = temp_dir / "file2.txt"
        file1.write_text("content1")
        file2.write_text("content2")

        output_dir = temp_dir / "output"
        image = (
            ImageInstance.from_registry("python:3.11")
            .add_local_file(str(file1), "/app/file1.txt")
            .add_local_file(str(file2), "/app/file2.txt")
        )
        build_dir = image.write(str(output_dir), name="test-image")

        assert (build_dir / "file1.txt").exists()
        assert (build_dir / "file2.txt").exists()
        assert (build_dir / "file1.txt").read_text() == "content1"
        assert (build_dir / "file2.txt").read_text() == "content2"


class TestImageAddLocalDir:
    """Tests for ImageInstance.add_local_dir() method."""

    def test_add_local_dir_copies_to_build_context(self, temp_source_dir, temp_dir):
        """Test that add_local_dir copies directory to build context."""
        output_dir = temp_dir / "output"
        image = ImageInstance.from_registry("python:3.11").add_local_dir(
            str(temp_source_dir), "/app", context_name="mydir"
        )
        build_dir = image.write(str(output_dir), name="test-image")
        copied_dir = build_dir / "mydir"

        assert copied_dir.exists()
        assert (copied_dir / "file1.txt").read_text() == "content1"
        assert (copied_dir / "file2.txt").read_text() == "content2"

    def test_add_local_dir_preserves_structure(self, temp_source_dir, temp_dir):
        """Test that add_local_dir preserves directory structure."""
        output_dir = temp_dir / "output"
        image = ImageInstance.from_registry("python:3.11").add_local_dir(
            str(temp_source_dir), "/app", context_name="mydir"
        )
        build_dir = image.write(str(output_dir), name="test-image")
        copied_dir = build_dir / "mydir"

        assert (copied_dir / "subdir").is_dir()
        assert (copied_dir / "subdir" / "nested.txt").read_text() == "nested content"

    def test_add_local_dir_overwrites_existing(self, temp_source_dir, temp_dir):
        """Test that add_local_dir overwrites existing directory."""
        output_dir = temp_dir / "output"
        output_dir.mkdir()

        # Build first time
        image = ImageInstance.from_registry("python:3.11").add_local_dir(
            str(temp_source_dir), "/app", context_name="mydir"
        )
        build_dir = image.write(str(output_dir), name="test-image")

        # Modify source
        (temp_source_dir / "file1.txt").write_text("modified")

        # Build again
        build_dir = image.write(str(output_dir), name="test-image")
        # Note: This should still have old content since we didn't recreate the image
        # But the directory copy should work without errors


class TestImageBuildContext:
    """Tests for ImageBuildContext dataclass."""

    def test_generate_dockerfile(self):
        """Test generate_dockerfile method."""
        context = ImageBuildContext(
            base_image="python:3.11",
            instructions=["WORKDIR /app", "RUN echo hello"],
        )
        dockerfile = context.generate_dockerfile()
        assert "FROM python:3.11" in dockerfile
        assert "WORKDIR /app" in dockerfile
        assert "RUN echo hello" in dockerfile

    def test_compute_hash(self):
        """Test compute_hash method."""
        context = ImageBuildContext(
            base_image="python:3.11",
            instructions=["WORKDIR /app"],
        )
        hash_value = context.compute_hash()
        assert len(hash_value) == 12  # First 12 chars of SHA256

    def test_empty_instructions(self):
        """Test with empty instructions."""
        context = ImageBuildContext(base_image="python:3.11")
        dockerfile = context.generate_dockerfile()
        assert "FROM python:3.11" in dockerfile

    def test_hash_includes_local_files(self, temp_file):
        """Test that hash includes local files metadata."""
        context1 = ImageBuildContext(
            base_image="python:3.11",
            local_files=[LocalFile(temp_file, "/app/file.txt", "file.txt")],
        )
        context2 = ImageBuildContext(
            base_image="python:3.11",
            local_files=[],
        )
        # Hashes should be different due to local file inclusion
        assert context1.compute_hash() != context2.compute_hash()


class TestLocalFile:
    """Tests for LocalFile dataclass."""

    def test_local_file_creation(self):
        """Test LocalFile dataclass creation."""
        local_file = LocalFile(
            source_path=Path("/tmp/test.txt"),
            destination_path="/app/test.txt",
            context_name="test.txt",
        )
        assert local_file.source_path == Path("/tmp/test.txt")
        assert local_file.destination_path == "/app/test.txt"
        assert local_file.context_name == "test.txt"


class TestDockerfileOrderPreservation:
    """Tests to verify Dockerfile instruction order is preserved."""

    def test_instruction_order_preserved(self):
        """Test that instructions appear in the correct order."""
        image = (
            ImageInstance.from_registry("python:3.11")
            .env(FIRST="1")
            .workdir("/app")
            .env(SECOND="2")
            .run_commands("echo middle")
            .env(THIRD="3")
        )
        dockerfile = image.dockerfile
        lines = dockerfile.split("\n")

        # Find indices of each instruction
        first_idx = next(i for i, line in enumerate(lines) if 'FIRST="1"' in line)
        workdir_idx = next(i for i, line in enumerate(lines) if "WORKDIR /app" in line)
        second_idx = next(i for i, line in enumerate(lines) if 'SECOND="2"' in line)
        run_idx = next(i for i, line in enumerate(lines) if "echo middle" in line)
        third_idx = next(i for i, line in enumerate(lines) if 'THIRD="3"' in line)

        assert first_idx < workdir_idx < second_idx < run_idx < third_idx


class TestSandboxApiPreparation:
    """Tests for sandbox-api injection functionality."""

    def test_prepare_for_sandbox_adds_sandbox_api(self):
        """Test that _prepare_for_sandbox adds sandbox-api COPY instruction."""
        image = ImageInstance.from_registry("python:3.11-slim")
        prepared = image._prepare_for_sandbox()

        assert "COPY --from=ghcr.io/blaxel-ai/sandbox:latest /sandbox-api /usr/local/bin/sandbox-api" in prepared.dockerfile

    def test_prepare_for_sandbox_adds_default_entrypoint(self):
        """Test that _prepare_for_sandbox adds default entrypoint if not set."""
        image = ImageInstance.from_registry("python:3.11-slim")
        prepared = image._prepare_for_sandbox()

        assert 'ENTRYPOINT ["/usr/local/bin/sandbox-api"]' in prepared.dockerfile

    def test_prepare_for_sandbox_preserves_user_entrypoint(self):
        """Test that user-defined entrypoint is preserved."""
        image = ImageInstance.from_registry("python:3.11-slim").entrypoint("/custom/entrypoint")
        prepared = image._prepare_for_sandbox()

        # User entrypoint should be present
        assert 'ENTRYPOINT ["/custom/entrypoint"]' in prepared.dockerfile
        # Default entrypoint should NOT be added
        assert prepared.dockerfile.count("ENTRYPOINT") == 1

    def test_prepare_for_sandbox_with_custom_version(self):
        """Test that custom sandbox version is used."""
        image = ImageInstance.from_registry("python:3.11-slim")
        prepared = image._prepare_for_sandbox("v1.2.3")

        assert "COPY --from=ghcr.io/blaxel-ai/sandbox:v1.2.3 /sandbox-api /usr/local/bin/sandbox-api" in prepared.dockerfile

    def test_prepare_for_sandbox_does_not_duplicate_sandbox_api(self):
        """Test that sandbox-api is not duplicated if already present."""
        # Image that does NOT have sandbox-api
        image = ImageInstance.from_registry("python:3.11-slim").run_commands(
            "echo 'hello world'"
        )
        # This image doesn't have sandbox-api
        assert not image._has_sandbox_api()

        # Now create one that does have it (base image is the sandbox image)
        image_with_api = ImageInstance.from_registry("ghcr.io/blaxel-ai/sandbox:latest")
        assert image_with_api._has_sandbox_api()

        prepared = image_with_api._prepare_for_sandbox()
        # Should not add another COPY instruction since base image is sandbox image
        # Count occurrences of the COPY instruction
        copy_count = prepared.dockerfile.count("COPY --from=ghcr.io/blaxel-ai/sandbox")
        assert copy_count == 0  # No new COPY added since base image already has it

    def test_has_sandbox_api_detects_sandbox_api_in_instructions(self):
        """Test _has_sandbox_api detects sandbox-api in Dockerfile."""
        image = ImageInstance.from_registry("python:3.11-slim")
        assert not image._has_sandbox_api()

        # Image with sandbox-api in a run command
        image_with_ref = image.run_commands("cp /sandbox-api /usr/bin/")
        assert image_with_ref._has_sandbox_api()

    def test_has_sandbox_api_detects_blaxel_sandbox_image(self):
        """Test _has_sandbox_api detects blaxel-ai/sandbox image reference."""
        image = ImageInstance.from_registry("ghcr.io/blaxel-ai/sandbox:latest")
        assert image._has_sandbox_api()

        image2 = ImageInstance.from_registry("python:3.11-slim")
        assert not image2._has_sandbox_api()

    def test_prepare_for_sandbox_returns_new_image(self):
        """Test that _prepare_for_sandbox returns a new Image instance (immutability)."""
        image = ImageInstance.from_registry("python:3.11-slim")
        prepared = image._prepare_for_sandbox()

        assert image is not prepared
        # Original should not have sandbox-api
        assert "sandbox-api" not in image.dockerfile
        # Prepared should have it
        assert "sandbox-api" in prepared.dockerfile

    def test_prepare_for_sandbox_preserves_all_instructions(self):
        """Test that all original instructions are preserved after preparation."""
        image = (
            ImageInstance.from_registry("python:3.11-slim")
            .run_commands("apt-get update && apt-get install -y curl git")
            .workdir("/app")
            .run_commands("pip install requests")
            .env(DEBUG="true")
        )
        prepared = image._prepare_for_sandbox()

        # All original instructions should be present
        assert "apt-get install" in prepared.dockerfile
        assert "WORKDIR /app" in prepared.dockerfile
        assert "pip install" in prepared.dockerfile
        assert 'DEBUG="true"' in prepared.dockerfile
        # Plus sandbox-api
        assert "sandbox-api" in prepared.dockerfile

    def test_entrypoint_sets_has_entrypoint_flag(self):
        """Test that entrypoint() sets the has_entrypoint flag."""
        image = ImageInstance.from_registry("python:3.11-slim")
        assert not image._context.has_entrypoint

        image_with_entrypoint = image.entrypoint("/app/start.sh")
        assert image_with_entrypoint._context.has_entrypoint

    def test_has_entrypoint_preserved_through_chaining(self):
        """Test that has_entrypoint flag is preserved through method chaining."""
        image = (
            ImageInstance.from_registry("python:3.11-slim")
            .entrypoint("/custom/entry")
            .workdir("/app")
            .env(FOO="bar")
        )
        assert image._context.has_entrypoint

    def test_sandbox_api_added_at_end_of_dockerfile(self):
        """Test that sandbox-api instructions are added at the end."""
        image = (
            ImageInstance.from_registry("python:3.11-slim")
            .workdir("/app")
            .run_commands("echo test")
        )
        prepared = image._prepare_for_sandbox()

        lines = [line for line in prepared.dockerfile.split("\n") if line.strip()]
        # COPY sandbox-api should be near the end
        copy_idx = next(i for i, line in enumerate(lines) if "COPY --from=" in line and "sandbox-api" in line)
        entrypoint_idx = next(i for i, line in enumerate(lines) if "ENTRYPOINT" in line)

        # Both should be after the RUN command
        run_idx = next(i for i, line in enumerate(lines) if "echo test" in line)
        assert copy_idx > run_idx
        assert entrypoint_idx > run_idx
        # Entrypoint should be last
        assert entrypoint_idx > copy_idx
