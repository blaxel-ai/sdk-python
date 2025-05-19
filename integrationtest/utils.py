import logging
import os

from blaxel.client.models import Metadata, Port, Runtime, Sandbox, SandboxSpec
from blaxel.sandbox.sandbox import SandboxInstance

logger = logging.getLogger(__name__)

async def local_sandbox(sandbox_name: str):
    os.environ[f"BL_SANDBOX_{sandbox_name.replace('-', '_').upper()}_URL"] = "http://localhost:8080"
    sandbox = SandboxInstance(Sandbox(
        metadata=Metadata(name=sandbox_name),
    ))
    return sandbox

async def create_or_get_sandbox(sandbox_name: str):
    # Create sandbox
    # return await local_sandbox(sandbox_name)
    try:
        sandbox = await SandboxInstance.get(sandbox_name)
        return sandbox
    except Exception:
        image = "blaxel/prod-base:latest"
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