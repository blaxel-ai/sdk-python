from blaxel.core.sandbox.client.models import ProcessRequest

process = ProcessRequest.from_dict(
    {"command": "ls -la", "env": {"PORT": "3000"}, "working_dir": "/home/user"}
)
assert process.working_dir == "/home/user"

process = ProcessRequest.from_dict(
    {"command": "ls -la", "env": {"PORT": "3000"}, "workingDir": "/home/user2"}
)
assert process.working_dir == "/home/user2"
