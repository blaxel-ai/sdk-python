import asyncio
import logging
import random
import string

from utils import create_or_get_sandbox

from blaxel.sandbox.client.models import ProcessRequest
from blaxel.sandbox.sandbox import SandboxInstance

logger = logging.getLogger(__name__)


def random_string(length: int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)).lower()


async def run_process_with_retry(sandbox: SandboxInstance, command: str):
    for _ in range(2):
        try:
            # new_client = client.with_base_url(sandbox.process.url).with_headers(settings.headers)
            # response = await new_client.get_async_httpx_client().get(f"/health")
            # print(response.text)
            dir = await sandbox.fs.ls("/")
            print(dir)
            process = await sandbox.process.exec(ProcessRequest(name="test", command=command))
            print(f"Process {process.name} started with pid {process.pid}")
            return process
        except Exception as e:
            print("Failed to run process, retrying...", e)
            await asyncio.sleep(1)

async def main():
    sandbox_name = random_string(10)
    try:
        print(f"Creating sandbox {sandbox_name}")
        sandbox = await create_or_get_sandbox(sandbox_name)
        sandbox = await SandboxInstance.get(sandbox_name)
        await run_process_with_retry(sandbox, 'pwd')
        await SandboxInstance.delete(sandbox_name)
    except Exception as e:
        print(e)
    finally:
        await SandboxInstance.delete(sandbox_name)

    sandbox_name = random_string(10)
    try:
        print(f"Creating sandbox {sandbox_name}")
        sandbox = await create_or_get_sandbox(sandbox_name)
        sandbox = await SandboxInstance.get(sandbox_name)
        await run_process_with_retry(sandbox, 'pwd')
        await SandboxInstance.delete(sandbox_name)
    except Exception as e:
        print(e)
    finally:
        await SandboxInstance.delete(sandbox_name)


if __name__ == "__main__":
    asyncio.run(main())
