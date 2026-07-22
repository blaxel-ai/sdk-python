"""Pytest configuration for core integration tests."""

import asyncio

import pytest

from tests.helpers import default_labels

_TEST_RESOURCE_LABELS = default_labels.copy()


def _resource_labels(resource) -> dict[str, str]:
    """Return resource labels without assuming every list projection includes them."""
    metadata = getattr(resource, "metadata", None)
    labels = getattr(metadata, "labels", None)
    if isinstance(labels, dict):
        return labels
    return getattr(labels, "additional_properties", {}) or {}


def _is_test_resource(resource) -> bool:
    labels = _resource_labels(resource)
    return all(labels.get(key) == value for key, value in _TEST_RESOURCE_LABELS.items())


def _api_error(response) -> str | None:
    """Describe generated API error responses while accepting successful models."""
    from blaxel.core.client.models.error import Error

    if not isinstance(response, Error):
        return None
    return f"{response.code}: {response.error}"


def pytest_sessionfinish(session, exitstatus):
    """Clean up all test sandboxes after the test session ends.

    With pytest-xdist, this only runs on the master node after all workers finish.
    """
    # Skip cleanup on worker nodes (pytest-xdist). Workers have workerinput;
    # the master process does not.
    if hasattr(session.config, "workerinput"):
        return

    from blaxel.core.client.api.volumes.list_volumes import asyncio as list_volumes
    from blaxel.core.client.client import client
    from blaxel.core.client.pagination import get_page_data, get_page_meta, normalize_cursor
    from blaxel.core.sandbox import SandboxInstance
    from blaxel.core.volume import VolumeInstance
    from tests.helpers import wait_for_sandbox_deletion, wait_for_volume_deletion

    async def list_volume_candidates():
        """List newly written test-volume candidates with server-side search."""
        cursor = None
        candidates = []
        while True:
            response = await list_volumes(
                client=client,
                cursor=normalize_cursor(cursor),
                limit=50,
                q=_TEST_RESOURCE_LABELS["env"],
            )
            response_error = _api_error(response)
            if response_error:
                raise RuntimeError(response_error)
            if response is None:
                raise RuntimeError("volume list returned no response")

            candidates.extend(VolumeInstance(volume) for volume in get_page_data(response))
            meta = get_page_meta(response)
            if not bool(getattr(meta, "has_more", False)):
                return candidates

            next_cursor = getattr(meta, "next_cursor", None)
            if not isinstance(next_cursor, str) or not next_cursor:
                raise RuntimeError("volume list said it has more results without a next cursor")
            cursor = next_cursor

    async def cleanup_test_resources() -> list[str]:
        """Delete resources with the exact integration-test labels."""
        # Reset the shared client so cleanup gets an event-loop-local client.
        client._async_client = None

        print("\n🧹 Cleaning up test resources...")
        deleted_sandboxes = 0
        deleted_volumes = 0
        cleanup_errors: list[str] = []

        # Collect every matching sandbox before deleting so cursor pagination is
        # not mutated underneath the scan.
        try:
            sandbox_page = await SandboxInstance.list()
            sandboxes = [
                sandbox
                async for sandbox in sandbox_page.auto_paging_iter()
                if _is_test_resource(sandbox)
            ]
        except Exception as error:
            cleanup_errors.append(f"listing sandboxes: {error}")
            sandboxes = []

        for sandbox in sandboxes:
            name = sandbox.metadata.name
            try:
                delete_error = _api_error(await sandbox.delete())
                if delete_error:
                    cleanup_errors.append(f"deleting sandbox {name}: {delete_error}")
                    continue
                if not await wait_for_sandbox_deletion(name):
                    cleanup_errors.append(f"deleting sandbox {name}: timed out")
                    continue
                deleted_sandboxes += 1
            except Exception as error:
                cleanup_errors.append(f"deleting sandbox {name}: {error}")

        # Volume list responses intentionally use LiteVolumeMetadata, which has
        # no labels. Search narrows the scan to newly written rows whose haystack
        # contains the test label, then GET provides labels for an exact match.
        # Collect every page before deleting so pagination is not mutated.
        try:
            listed_volumes = await list_volume_candidates()
        except Exception as error:
            cleanup_errors.append(f"listing volumes: {error}")
            listed_volumes = []

        volumes = []
        for listed_volume in listed_volumes:
            name = listed_volume.name
            if not isinstance(name, str) or not name:
                cleanup_errors.append("inspecting volume: list response omitted its name")
                continue
            try:
                volume = await VolumeInstance.get(name)
            except Exception as error:
                cleanup_errors.append(f"inspecting volume {name}: {error}")
                continue
            if _is_test_resource(volume):
                volumes.append(volume)

        for volume in volumes:
            name = volume.name
            try:
                delete_error = _api_error(await volume.delete())
                if delete_error:
                    cleanup_errors.append(f"deleting volume {name}: {delete_error}")
                    continue
                if not await wait_for_volume_deletion(name):
                    cleanup_errors.append(f"deleting volume {name}: timed out")
                    continue
                deleted_volumes += 1
            except Exception as error:
                cleanup_errors.append(f"deleting volume {name}: {error}")

        # Discard the loop-bound client after cleanup.
        client._async_client = None

        print(f"  Deleted {deleted_sandboxes} sandbox(es) and {deleted_volumes} volume(s).")
        return cleanup_errors

    try:
        cleanup_errors = asyncio.run(cleanup_test_resources())
    except Exception as error:
        cleanup_errors = [f"cleanup crashed: {error}"]

    if cleanup_errors:
        for error in cleanup_errors:
            print(f"  Cleanup error: {error}")
        print("❌ Cleanup incomplete.")
        session.exitstatus = pytest.ExitCode.TESTS_FAILED
    else:
        print("✅ Cleanup complete!")
