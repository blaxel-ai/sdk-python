import os
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from blaxel.core.client.models import Metadata, Port, Runtime, Sandbox, SandboxSpec
from blaxel.core.sandbox import SandboxInstance

sep = "--------------------------------"


def info(msg: str) -> None:
    """Print info message with [INFO] prefix."""
    print(f"[INFO] {msg}")


async def local_sandbox(sandbox_name: str) -> SandboxInstance:
    """Create a local sandbox instance for testing."""
    env_var = f"BL_SANDBOXES_{sandbox_name.replace('-', '_').upper()}_URL"
    os.environ[env_var] = "http://localhost:8080"

    sandbox = SandboxInstance(Sandbox(metadata=Metadata(name=sandbox_name)))
    return sandbox


async def create_or_get_sandbox(
    sandbox_name: str,
    image: str = "blaxel/prod-nextjs:latest",
    ports: Optional[List[Dict[str, Any]]] = None,
    memory: int = 4096,
    envs: Optional[List[Dict[str, str]]] = None,
) -> SandboxInstance:
    """Create or get existing sandbox with specified configuration."""
    # Uncomment the line below to use local sandbox instead
    # return await local_sandbox(sandbox_name)

    if ports is None:
        ports = []

    if envs is None:
        envs = []

    if not ports:
        ports = [
            {
                "name": "expo-web",
                "target": 8081,
                "protocol": "HTTP",
            },
            {
                "name": "preview",
                "target": 3000,
                "protocol": "HTTP",
            },
        ]

    # Convert port dictionaries to Port model objects
    port_objects = [
        Port(name=port["name"], target=port["target"], protocol=port["protocol"]) for port in ports
    ]

    # Create proper model objects
    metadata = Metadata(name=sandbox_name)
    runtime = Runtime(image=image, memory=memory, ports=port_objects, envs=envs, generation="mk3")
    spec = SandboxSpec(runtime=runtime)
    sandbox_model = Sandbox(metadata=metadata, spec=spec)

    sandbox = await SandboxInstance.create_if_not_exists(sandbox_model)
    await sandbox.wait(max_wait=120000, interval=1000)
    return sandbox


async def run_command(
    sandbox: SandboxInstance,
    command: str,
    name: Optional[str] = None,
    max_wait: Optional[int] = None,
    working_dir: Optional[str] = None,
    wait_for_completion: bool = True,
) -> None:
    """Run a command in the sandbox and handle logging."""
    info(f"⚡ Running: {command}")

    process = await sandbox.process.exec(
        name=name,
        command=command,
        wait_for_completion=wait_for_completion,
        working_dir=working_dir,
    )

    process_name = name or process.name

    if not wait_for_completion:
        # Start streaming logs
        def on_log(log):
            print(f"[{process_name}] {log}")

        stream = sandbox.process.stream_logs(process_name, on_log=on_log)

        if max_wait:
            await sandbox.process.wait(process_name, max_wait=max_wait, interval=1000)

        stream.close()
    else:
        # Get logs after completion
        logs = await sandbox.process.logs(process_name, "all")
        if logs:
            print(f"--- Logs for {process_name} ---")
            print(logs)
            print(f"--- End logs for {process_name} ---")

    # Get final process status
    process = await sandbox.process.get(process_name)
    print(f"{process_name} status: {process.status if process else 'unknown'}")

    if process and process.status == "failed":
        print(f"{process_name} exit code: {process.exit_code}")
        logs = await sandbox.process.logs(process_name, "all")
        print(f"{process_name} logs: {logs}")


def create_zip_from_directory(source_dir: str, output_path: str) -> None:
    """Create a zip file from a directory, excluding common ignored folders."""
    source_path = Path(source_dir)
    dir_name = source_path.name

    # Folders to ignore
    ignored_folders = {"node_modules", ".next", ".DS_Store"}

    def should_ignore(path: Path) -> bool:
        """Check if path should be ignored."""
        return path.name in ignored_folders

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in source_path.rglob("*"):
            # Skip if any parent directory is in ignored folders
            if any(should_ignore(parent) for parent in file_path.parents):
                continue

            # Skip if the file/folder itself should be ignored
            if should_ignore(file_path):
                continue

            if file_path.is_file():
                # Calculate the archive path with directory name as root
                relative_path = file_path.relative_to(source_path)
                archive_path = Path(dir_name) / relative_path
                zip_file.write(file_path, archive_path)


async def create_preview(sandbox: SandboxInstance):
    """Create a preview for the sandbox."""
    preview = await sandbox.previews.create_if_not_exists(
        {"metadata": {"name": "preview-nextjs"}, "spec": {"port": 3000, "public": True}}
    )
    return preview


async def check_usage(sandbox: SandboxInstance) -> None:
    """Check sandbox resource usage (memory and disk space)."""
    print(sep)
    print("💰 Checking usage")

    # Check disk space
    disk_space = await sandbox.process.exec(
        name="disk-space", command="df -m", working_dir="/home/user"
    )

    # Check memory usage
    memory = await sandbox.process.exec(name="memory", command="free -m", working_dir="/home/user")

    # Get logs
    memory_logs = await sandbox.process.logs(memory.pid, "all")
    disk_space_logs = await sandbox.process.logs(disk_space.pid, "all")

    print(f"🧠 Memory:\n{memory_logs}")
    print(f"💾 Disk Space:\n{disk_space_logs}")
