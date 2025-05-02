import asyncio
import logging
import os

from blaxel.client.models import Metadata, Port, Runtime, Sandbox, SandboxSpec
from blaxel.sandbox.base import ResponseError
from blaxel.sandbox.client.models import ProcessRequest
from blaxel.sandbox.sandbox import SandboxInstance

logger = logging.getLogger(__name__)


async def create_sandbox(sandbox_name: str):
    # Create sandbox
    image = "blaxel/prod-base:14769328323"
    logger.info(f"Creating sandbox {sandbox_name} with image {image}")
    sandbox = await SandboxInstance.create(Sandbox(
        metadata=Metadata(name=sandbox_name),
        spec=SandboxSpec(
            runtime=Runtime(
                image=image,
                memory=2048,
                cpu=2,
                ports=[
                    Port(name="sandbox-api", target=8080, protocol="HTTP")
                ]
            )
        )
    ))
    logger.info("Waiting for sandbox to be deployed")
    await sandbox.wait(max_wait=120000, interval=1000)
    logger.info("Sandbox deployed")
    return sandbox

async def main():
    user = os.environ.get("USER")
    sandbox_name = "sandbox-test-3"
    sandbox = None
    try:
        sandbox = await create_sandbox(sandbox_name)
        sandbox = await SandboxInstance.get(sandbox_name)

        # Filesystem tests
        await sandbox.fs.write(f"/Users/{user}/Downloads/test", "Hello world")
        content = await sandbox.fs.read(f"/Users/{user}/Downloads/test")
        assert content == "Hello world", "File content is not correct"
        dir = await sandbox.fs.ls(f"/Users/{user}/Downloads")
        assert dir.files and len(dir.files) >= 1, "Directory is empty"
        assert any(f.path == f"/Users/{user}/Downloads/test" for f in dir.files), "File not found in directory"
        await sandbox.fs.mkdir(f"/Users/{user}/Downloads/test2")
        after_mkdir = await sandbox.fs.ls(f"/Users/{user}/Downloads/test2")
        assert not after_mkdir.files or len(after_mkdir.files) == 0, "Directory is not empty after mkdir"
        await sandbox.fs.cp(f"/Users/{user}/Downloads/test", f"/Users/{user}/Downloads/test2/test")
        after_cp_ls = await sandbox.fs.ls(f"/Users/{user}/Downloads/test2")
        assert after_cp_ls.files and any(f.path == f"/Users/{user}/Downloads/test2/test" for f in after_cp_ls.files), "File not found in directory after cp"
        await sandbox.fs.rm(f"/Users/{user}/Downloads/test")
        try:
            await sandbox.fs.rm(f"/Users/{user}/Downloads/test2")
        except ResponseError as e:
            logger.info(f"That is expected => {e.error}")
        await sandbox.fs.rm(f"/Users/{user}/Downloads/test2", True)

        # Process tests
        process = await sandbox.process.exec(ProcessRequest(name="test", command="echo 'Hello world'"))
        assert getattr(process, "status", None) != "completed", "Process did complete without waiting"
        await asyncio.sleep(0.01)
        completed_process = await sandbox.process.get("test")
        assert getattr(completed_process, "status", None) == "completed", "Process did not complete"
        logs = await sandbox.process.logs("test")
        assert logs == 'Hello world\n', "Logs are not correct"
        try:
            await sandbox.process.kill("test")
        except ResponseError as e:
            logger.info(f"That is expected => {e.error}")
    finally:
        logger.info("Deleting sandbox")
        await SandboxInstance.delete(sandbox_name)

if __name__ == "__main__":
    asyncio.run(main())
