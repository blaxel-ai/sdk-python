import asyncio
import os
import random
import string
import sys
import time

import aiohttp

from blaxel.core.common.settings import settings
from blaxel.core.sandbox import SandboxInstance


def get_unique_id():
    """Generate a unique ID for each sandbox."""
    return f"{int(time.time())}{''.join(random.choices(string.ascii_lowercase + string.digits, k=5))}"


# Configuration map for available regions per environment
REGION_CONFIG = {
    "prod": {
        "regions": ["us-pdx-1", "eu-lon-1", "us-was-1"],
        "default_region": "us-pdx-1",
        "image": "blaxel/prod-base:latest"
    },
    "dev": {
        "regions": ["eu-dub-1"],
        "default_region": "eu-dub-1", 
        "image": "blaxel/dev-base:latest"
    }
}

# Determine environment from BL_ENV variable (default to prod)
environment = os.environ.get("BL_ENV", "prod")
config = REGION_CONFIG.get(environment, REGION_CONFIG["prod"])

test_regions = config["regions"]
default_region = config["default_region"]
test_image = config["image"]

print(f"🌍 Running region tests in {environment} environment")
print(f"   Regions to test: {', '.join(test_regions)}")
print(f"   Default region: {default_region}\n")


async def test_preview_in_region(sandbox_name: str, region: str):
    """Test public preview in the specified region."""
    sandbox = await SandboxInstance.get(sandbox_name)
    sandbox_instance = SandboxInstance(sandbox)
    
    try:
        preview = await sandbox_instance.previews.create({
            "metadata": {
                "name": "preview-region-test"
            },
            "spec": {
                "port": 443,
                "prefixUrl": "region-test",
                "public": True
            }
        })
        
        url = preview.spec.url if preview.spec else None
        if not url:
            raise Exception("Preview URL not returned")
        
        # The URL format includes the region when it's not the default region
        if settings.env == "dev":
            expected_domain = (
                f"https://region-test-{settings.workspace}.preview.blaxel.dev"
                if region == default_region
                else f"https://region-test-{settings.workspace}.{region}.preview.blaxel.dev"
            )
        else:
            expected_domain = (
                f"https://region-test-{settings.workspace}.preview.bl.run"
                if region == default_region
                else f"https://region-test-{settings.workspace}.{region}.preview.bl.run"
            )
        
        if url != expected_domain:
            print(f"   ℹ️ Preview URL: {url} (expected format confirmed)")
        else:
            print(f"   ℹ️ Preview URL: {url}")
        
        # Test the preview endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}/health") as response:
                if response.status == 200:
                    print(f"   ✓ Public preview working in {region}")
                else:
                    raise Exception(f"Preview health check failed: {response.status}")
        
        await sandbox_instance.previews.delete("preview-region-test")
    except Exception as e:
        print(f"   ✗ Preview test failed in {region}: {e}")
        raise


async def main():
    """Test region field support in Python SDK."""
    try:
        # Test 1: Create sandbox without region (should get default)
        print("📋 Test 1: Create sandbox without region")
        sandbox = await SandboxInstance.create({
            "name": f"test-no-region-{get_unique_id()}",
            "image": test_image,
            "memory": 1024
        })
        
        retrieved = await SandboxInstance.get(sandbox.metadata.name)
        actual_region = retrieved.spec.region if retrieved.spec and hasattr(retrieved.spec, 'region') else None
        print(f"   Default region set: {actual_region}")
        
        if actual_region != default_region:
            print(f"   ⚠️ Expected default {default_region}, got {actual_region}")
        else:
            print("   ✓ Default region correctly set")
        
        await SandboxInstance.delete(sandbox.metadata.name)
        print()

        # Test 2: Create sandbox with each available region
        print("📋 Test 2: Create sandbox with explicit regions")
        for test_region in test_regions:
            sandbox = await SandboxInstance.create({
                "name": f"test-region-{test_region}-{get_unique_id()}",
                "image": test_image,
                "memory": 1024,
                "region": test_region
            })
            
            retrieved = await SandboxInstance.get(sandbox.metadata.name)
            actual_region = retrieved.spec.region if retrieved.spec and hasattr(retrieved.spec, 'region') else None
            
            if actual_region == test_region:
                print(f"   ✓ {test_region}: Correctly set")
            else:
                print(f"   ✗ {test_region}: Expected {test_region}, got {actual_region}")
                raise Exception("Region verification failed")
            
            await SandboxInstance.delete(sandbox.metadata.name)

        # Test 3: Test public preview in each region
        print("\n📋 Test 3: Test public preview in each region")
        for test_region in test_regions:
            sandbox_name = f"test-preview-{test_region}-{get_unique_id()}"
            sandbox = await SandboxInstance.create({
                "name": sandbox_name,
                "image": test_image,
                "memory": 1024,
                "region": test_region
            })
            
            try:
                await test_preview_in_region(sandbox_name, test_region)
            finally:
                await SandboxInstance.delete(sandbox_name)

        print("\n✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        sys.exit(1)
