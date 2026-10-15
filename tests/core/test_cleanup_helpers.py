"""Unit tests for the integration-suite cleanup predicates.

The session teardown decides what to delete in a workspace shared with other
CI runs, so a parsing slip here either leaves orphans forever or, worse, deletes
someone else's sandbox.
"""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from tests.helpers import ORPHAN_MAX_AGE, is_stale_orphan, resource_labels

NOW = datetime(2026, 8, 18, 12, 0, 0, tzinfo=timezone.utc)


def _resource(created_at=None, labels=None):
    metadata = SimpleNamespace(created_at=created_at)
    if labels is not None:
        metadata.labels = SimpleNamespace(additional_properties=labels)
    return SimpleNamespace(metadata=metadata)


class TestIsStaleOrphan:
    def test_accepts_every_timestamp_shape_the_api_returns(self):
        """RFC3339 with a Z, with or without a fraction, up to nanoseconds."""
        old = NOW - ORPHAN_MAX_AGE - timedelta(minutes=1)
        stamp = old.strftime("%Y-%m-%dT%H:%M:%S")
        for created_at in (
            f"{stamp}Z",
            f"{stamp}.123Z",
            f"{stamp}.123456Z",
            f"{stamp}.03583072Z",
        ):
            assert is_stale_orphan(_resource(created_at), now=NOW) is True, created_at

    def test_recent_resource_is_not_stale(self):
        """A live concurrent run must never have its sandboxes swept."""
        recent = (NOW - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S.123456Z")
        assert is_stale_orphan(_resource(recent), now=NOW) is False

    def test_boundary_is_exclusive(self):
        exactly = (NOW - ORPHAN_MAX_AGE).strftime("%Y-%m-%dT%H:%M:%SZ")
        assert is_stale_orphan(_resource(exactly), now=NOW) is False

    def test_unparsable_timestamp_fails_safe(self):
        """Anything we cannot read is treated as live, never deleted."""
        assert is_stale_orphan(_resource("not-a-date"), now=NOW) is False
        assert is_stale_orphan(_resource(None), now=NOW) is False
        assert is_stale_orphan(SimpleNamespace(metadata=None), now=NOW) is False


class TestResourceLabels:
    def test_reads_labels_from_additional_properties(self):
        assert resource_labels(_resource(labels={"run-id": "abc"})) == {"run-id": "abc"}

    def test_missing_labels_yield_empty_dict(self):
        """Volume listings return metadata without a labels attribute at all."""
        assert resource_labels(_resource()) == {}
        assert resource_labels(SimpleNamespace(metadata=None)) == {}
