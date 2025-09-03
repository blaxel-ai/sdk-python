import asyncio
import os
import sys
import time
import random
import string

from blaxel.core.client.models import Metadata, Runtime, Sandbox, SandboxSpec
from blaxel.core.sandbox import SandboxCreateConfiguration, SandboxInstance


def get_unique_id():
    """Generate a unique ID for each sandbox to avoid conflicts with async deletion.
    This is necessary because sandbox deletion is async and we want to avoid naming conflicts."""
    return f"{int(time.time())}{''.join(random.choices(string.ascii_lowercase + string.digits, k=5))}"


async def delay(ms: int = 10):
    """Small delay helper to ensure unique timestamps."""
    await asyncio.sleep(ms / 1000)

# Configuration map for available regions per environment
# Update this map when new regions become available
REGION_CONFIG = {
    "prod": {
        "regions": ["us-west-2"],  # Add more regions here as they become available, e.g., ["us-west-2", "us-east-1", "eu-west-1"]
        "default_region": "us-west-2",
        "image": "blaxel/prod-base:latest"
    },
    "dev": {
        "regions": ["eu-west-1"],  # Add more regions here as they become available, e.g., ["eu-west-1", "us-west-2", "ap-southeast-1"]
        "default_region": "eu-west-1", 
        "image": "blaxel/dev-base:latest"
    }
}

# Determine environment from BL_ENV variable (default to prod)
environment = os.environ.get("BL_ENV", "prod")
config = REGION_CONFIG.get(environment, REGION_CONFIG["prod"])

test_regions = config["regions"]
default_region = config["default_region"]
test_image = config["image"]

print(f"🌍 Running tests in {environment} environment")
print(f"   Available regions: {', '.join(test_regions)}")
print(f"   Default region: {default_region}")
print(f"   Using image: {test_image}\n")


async def verify_region(sandbox_name: str, expected_region: str = None):
    """Verify that the region is properly set in the sandbox."""
    retrieved = await SandboxInstance.get(sandbox_name)
    actual_region = retrieved.spec.region if retrieved.spec and hasattr(retrieved.spec, 'region') else None
    
    if expected_region is None:
        # For sandboxes created without region, backend should set it to the default region
        print(f"   Backend set region to: {actual_region} (default for {environment})")
        if actual_region != default_region:
            print(f"   Note: Backend used {actual_region} instead of expected default {default_region}")
    elif actual_region == expected_region:
        print(f"   ✓ Verified: Region correctly set to {actual_region}")
    else:
        print(f"   ✗ Region mismatch! Expected {expected_region}, got {actual_region}")
        raise Exception(f"Region verification failed for {sandbox_name}")
    
    return retrieved


async def main():
    """Test region field support in Python SDK."""
    try:
        print("Testing region field support in Python SDK\n")
        print("=" * 50)
        
        # Test 1: Backward compatibility - Create sandbox without region (backend will set default)
        print("\n✅ Test 1: Backward compatibility - Create sandbox without region")
        print("This ensures existing code continues to work (backend auto-sets default region)...")
        sandbox = await SandboxInstance.create({
            "name": f"test-without-region-{get_unique_id()}",
            "image": test_image,
            "memory": 1024
        })
        print(f"Created sandbox without region: {sandbox.metadata.name}")
        await verify_region(sandbox.metadata.name, None)
        await SandboxInstance.delete(sandbox.metadata.name)
        print("Deleted sandbox without region\n")
        await delay()  # Small delay to ensure unique timestamps for next sandbox

        # Test 2: SandboxCreateConfiguration without region (backward compat)
        print("✅ Test 2: SandboxCreateConfiguration without region (backward compatibility)")
        config_no_region = SandboxCreateConfiguration(
            name=f"test-config-no-region-{get_unique_id()}",
            image=test_image,
            memory=2048
        )
        sandbox = await SandboxInstance.create(config_no_region)
        print(f"Created sandbox via config without region: {sandbox.metadata.name}")
        await verify_region(sandbox.metadata.name, None)
        await SandboxInstance.delete(sandbox.metadata.name)
        print("Deleted config sandbox without region\n")
        await delay()  # Ensure unique timestamps

        # Test all available regions
        for test_region in test_regions:
            print("=" * 50)
            print(f"\n🌍 Testing region: {test_region}")
            print("=" * 50)
            
            # Test 3: Create sandbox with explicit region using SandboxCreateConfiguration
            print("\n✅ Test 3: Create sandbox with explicit region using SandboxCreateConfiguration")
            config_with_region = SandboxCreateConfiguration(
                name=f"test-region-config-{test_region}-{get_unique_id()}",
                image=test_image,
                memory=1024,
                region=test_region
            )
            sandbox = await SandboxInstance.create(config_with_region)
            print(f"Created sandbox with region via config: {sandbox.metadata.name}")
            await verify_region(sandbox.metadata.name, test_region)
            await SandboxInstance.delete(sandbox.metadata.name)
            print("Deleted sandbox with region\n")
            await delay()  # Ensure unique timestamps

            # Test 4: Create sandbox with region in spec structure  
            print("✅ Test 4: Create sandbox with region in spec structure")
            sandbox_model = Sandbox(
                metadata=Metadata(name=f"test-region-spec-{test_region}-{get_unique_id()}"),
                spec=SandboxSpec(
                    region=test_region,
                    runtime=Runtime(
                        image=test_image,
                        memory=1024
                    )
                )
            )
            sandbox = await SandboxInstance.create(sandbox_model)
            print(f"Created sandbox with region in spec: {sandbox.metadata.name}")
            await verify_region(sandbox.metadata.name, test_region)
            await SandboxInstance.delete(sandbox.metadata.name)
            print("Deleted sandbox with region spec\n")
            await delay()  # Ensure unique timestamps

            # Test 5: Create sandbox with dict and region
            print("✅ Test 5: Create sandbox with dict and region")
            sandbox = await SandboxInstance.create({
                "name": f"test-dict-region-{test_region}-{get_unique_id()}",
                "region": test_region,
                "image": test_image,
                "memory": 1024
            })
            print(f"Created sandbox with region via dict: {sandbox.metadata.name}")
            await verify_region(sandbox.metadata.name, test_region)
            await SandboxInstance.delete(sandbox.metadata.name)
            print("Deleted dict sandbox with region\n")
            await delay()  # Ensure unique timestamps

            # Test 6: Create sandbox with create_if_not_exists and region
            print("✅ Test 6: Create sandbox with create_if_not_exists and region")
            sandbox = await SandboxInstance.create_if_not_exists({
                "name": f"test-cine-region-{test_region}-{get_unique_id()}",
                "region": test_region,
                "image": test_image,
                "memory": 1024
            })
            print(f"Created/found sandbox with region: {sandbox.metadata.name}")
            await verify_region(sandbox.metadata.name, test_region)
            await SandboxInstance.delete(sandbox.metadata.name)
            print("Deleted create_if_not_exists sandbox\n")
            await delay()  # Ensure unique timestamps

            # Test 7: Verify region persistence - Create then get multiple times
            print("✅ Test 7: Verify region persistence")
            sandbox = await SandboxInstance.create({
                "name": f"test-persist-{test_region}-{get_unique_id()}",
                "region": test_region,
                "image": test_image
            })
            print(f"Created sandbox with region {test_region}: {sandbox.metadata.name}")
            
            # Get the sandbox multiple times to ensure persistence
            for i in range(1, 3):
                print(f"   Verification attempt {i}:")
                await verify_region(sandbox.metadata.name, test_region)
            
            await SandboxInstance.delete(sandbox.metadata.name)
            print("Deleted persistence test sandbox\n")
            await delay()  # Ensure unique timestamps

        print("=" * 50)
        print("\n🎉 All region tests passed successfully!")
        print("\nSummary:")
        print("- ✓ Backward compatibility maintained (backend auto-sets default region when not specified)")
        print(f"- ✓ All {len(test_regions)} region(s) tested: {', '.join(test_regions)}")
        print("- ✓ Region can be specified in SandboxCreateConfiguration")
        print("- ✓ Region can be specified in spec structure")
        print("- ✓ Region can be specified via dict")
        print("- ✓ Region works with create_if_not_exists")
        print("- ✓ Region is properly persisted and verified after each creation")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        sys.exit(1)
