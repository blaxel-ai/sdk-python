import asyncio
import sys

from blaxel.core.sandbox import SandboxCreateConfiguration, SandboxInstance


async def main():
    """Test various sandbox creation scenarios."""
    try:
        # Test 1: Create sandbox with no parameters (should use defaults)
        print("Test 1: Create sandbox with default parameters...")
        sandbox = await SandboxInstance.create()
        await sandbox.wait()
        print(f"✅ Created sandbox with default name: {sandbox.metadata.name}")
        print(await sandbox.fs.ls("/blaxel"))
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✅ Deleted default sandbox")

        # Test 2: Create sandbox with spec containing runtime image
        print("\nTest 2: Create sandbox with spec runtime...")
        sandbox = await SandboxInstance.create(
            {"spec": {"runtime": {"image": "blaxel/prod-base:latest"}}}
        )
        await sandbox.wait()
        print(f"✅ Created sandbox with spec: {sandbox.metadata.name}")
        print(await sandbox.fs.ls("/blaxel"))
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✅ Deleted spec sandbox")

        # Test 3: Create sandbox with simplified name configuration
        print("\nTest 3: Create sandbox with name configuration...")
        sandbox = await SandboxInstance.create({"name": "sandbox-with-name"})
        await sandbox.wait()
        print(f"✅ Created sandbox with name: {sandbox.metadata.name}")
        print(await sandbox.fs.ls("/blaxel/"))
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✅ Deleted named sandbox")

        # Test 4: Create sandbox using SandboxCreateConfiguration
        print("\nTest 4: Create sandbox with SandboxCreateConfiguration...")
        config = SandboxCreateConfiguration(name="sandbox-config-test")
        sandbox = await SandboxInstance.create(config)
        await sandbox.wait()
        print(f"✅ Created sandbox with config: {sandbox.metadata.name}")
        print(await sandbox.fs.ls("/blaxel/"))
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✅ Deleted config sandbox")

        # Test 5: Create sandbox if not exists with name
        print("\nTest 5: Create sandbox if not exists with name...")
        sandbox = await SandboxInstance.create_if_not_exists({"name": "sandbox-cine-name"})
        await sandbox.wait()
        print(f"✅ Created/found sandbox: {sandbox.metadata.name}")
        print(await sandbox.fs.ls("/blaxel/"))
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✅ Deleted create-if-not-exists sandbox")

        # Test 6: Create sandbox if not exists with metadata structure
        print("\nTest 6: Create sandbox if not exists with metadata...")
        sandbox = await SandboxInstance.create_if_not_exists(
            {"metadata": {"name": "sandbox-cine-metadata"}}
        )
        await sandbox.wait()
        print(f"✅ Created/found sandbox with metadata: {sandbox.metadata.name}")
        print(await sandbox.fs.ls("/blaxel/"))
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✅ Deleted metadata sandbox")

        # Test 7: Create sandbox with custom image and memory
        print("\nTest 7: Create sandbox with custom image and memory...")
        custom_config = SandboxCreateConfiguration(
            name="sandbox-custom",
            image="blaxel/prod-base:latest",
            memory=2048,
        )
        sandbox = await SandboxInstance.create(custom_config)
        await sandbox.wait()
        print(f"✅ Created custom sandbox: {sandbox.metadata.name}")
        print(f"   Image: {sandbox.spec.runtime.image}")
        print(f"   Memory: {sandbox.spec.runtime.memory}")
        print(await sandbox.fs.ls("/blaxel/"))
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✅ Deleted custom sandbox")

        # Test 8: Create sandbox with ports
        print("\nTest 8: Create sandbox with ports...")
        ports_config = SandboxCreateConfiguration(
            name="sandbox-with-ports",
            image="blaxel/prod-base:latest",
            memory=2048,
            ports=[
                {"name": "web", "target": 3000},  # Will default to HTTP
                {"name": "api", "target": 8080, "protocol": "TCP"},
            ],
        )
        sandbox = await SandboxInstance.create(ports_config)
        await sandbox.wait()
        print(f"✅ Created sandbox with ports: {sandbox.metadata.name}")
        print(f"   Image: {sandbox.spec.runtime.image}")
        print(f"   Memory: {sandbox.spec.runtime.memory}")
        sandbox = await SandboxInstance.get(sandbox.metadata.name)
        if sandbox.spec.runtime.ports:
            print(f"   Ports: {len(sandbox.spec.runtime.ports)} configured")
            for port in sandbox.spec.runtime.ports:
                print(f"     - {port.name}: {port.target} ({port.protocol})")
        print(await sandbox.fs.ls("/blaxel/"))
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✅ Deleted ports sandbox")

        # Test 9: Create sandbox with environment variables
        print("\nTest 9: Create sandbox with environment variables...")
        envs_config = SandboxCreateConfiguration(
            name="sandbox-with-envs",
            image="blaxel/prod-base:latest",
            memory=2048,
            envs=[
                {"name": "NODE_ENV", "value": "development"},
                {"name": "DEBUG", "value": "true"},
                {"name": "API_KEY", "value": "secret123"},
                {"name": "PORT", "value": "3000"},
            ],
        )
        sandbox = await SandboxInstance.create(envs_config)
        await sandbox.wait()
        print(f"✅ Created sandbox with envs: {sandbox.metadata.name}")
        print(f"   Image: {sandbox.spec.runtime.image}")
        print(f"   Memory: {sandbox.spec.runtime.memory}")
        sandbox = await SandboxInstance.get(sandbox.metadata.name)
        if sandbox.spec.runtime.envs:
            print(f"   Envs: {len(sandbox.spec.runtime.envs)} configured")
            for env in sandbox.spec.runtime.envs:
                print(f"     - {env['name']}: {env['value']}")
        print(await sandbox.fs.ls("/blaxel/"))
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✅ Deleted envs sandbox")

        # Test 10: Create sandbox with environment variables using dict syntax
        print("\nTest 10: Create sandbox with envs using dict syntax...")
        sandbox = await SandboxInstance.create({
            "name": "sandbox-with-envs-dict",
            "image": "blaxel/prod-base:latest",
            "memory": 2048,
            "envs": [
                {"name": "ENVIRONMENT", "value": "test"},
                {"name": "VERSION", "value": "1.0.0"},
            ]
        })
        await sandbox.wait()
        print(f"✅ Created sandbox with envs dict: {sandbox.metadata.name}")
        print(f"   Image: {sandbox.spec.runtime.image}")
        print(f"   Memory: {sandbox.spec.runtime.memory}")
        sandbox = await SandboxInstance.get(sandbox.metadata.name)
        if sandbox.spec.runtime.envs:
            print(f"   Envs: {len(sandbox.spec.runtime.envs)} configured")
            for env in sandbox.spec.runtime.envs:
                print(f"     - {env['name']}: {env['value']}")
        print(await sandbox.fs.ls("/blaxel/"))
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✅ Deleted envs dict sandbox")

        print("\n🎉 All sandbox creation tests passed!")

    except Exception as e:
        print(f"❌ There was an error => {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("✅ Tests completed successfully")
        sys.exit(0)
    except Exception as err:
        print(f"❌ There was an error => {err}")
        sys.exit(1)
