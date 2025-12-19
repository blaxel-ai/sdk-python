"""Tests for snake_case to camelCase conversion support."""

from blaxel.core.sandbox.client.models import ProcessRequest


def test_process_request_accepts_snake_case():
    """Test that ProcessRequest accepts snake_case parameters."""
    process = ProcessRequest.from_dict(
        {"command": "ls -la", "env": {"PORT": "3000"}, "working_dir": "/home/user"}
    )
    assert process.working_dir == "/home/user"


def test_process_request_accepts_camel_case():
    """Test that ProcessRequest accepts camelCase parameters."""
    process = ProcessRequest.from_dict(
        {"command": "ls -la", "env": {"PORT": "3000"}, "workingDir": "/home/user2"}
    )
    assert process.working_dir == "/home/user2"
