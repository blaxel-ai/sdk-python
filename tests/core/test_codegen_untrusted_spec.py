"""Our custom templates must not turn OpenAPI strings into code (GHSA-5293-mq8x-g3xj).

Generates a client from a spec whose names, descriptions, enum values and defaults try
to break out of string literals, then imports the generated models and checks that
nothing ran. Skipped where the generator (Python 3.11+, dev group) is not installed.
"""

import importlib
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("openapi_python_client")

REPO = Path(__file__).resolve().parents[2]


def _spec(marker: Path) -> str:
    run = f'__import__("os").system("touch {marker}")'
    return f"""
openapi: 3.0.0
info: {{title: 'evil \"\"\" + {run} + \"\"\"', version: "1"}}
paths:
  '/things/{{name}}"+{run}+"':
    get:
      operationId: getThing
      description: 'desc \"\"\"; {run}; \"\"\"'
      parameters:
        - {{name: name, in: path, required: true, schema: {{type: string}}}}
      responses:
        "200": {{description: ok}}
components:
  schemas:
    Kind:
      type: string
      enum: ['a", {run}, "', b]
    Thing:
      type: object
      description: 'x \"\"\" ; {run} ; \"\"\"'
      properties:
        'weirdName") or {run} or ("': {{type: string}}
        kind: {{$ref: "#/components/schemas/Kind"}}
        other: {{type: string, default: '"; {run}; "'}}
"""


def test_hostile_spec_strings_stay_strings(tmp_path):
    marker = tmp_path / "pwned"
    spec = tmp_path / "spec.yml"
    spec.write_text(_spec(marker))
    config = tmp_path / "config.yml"
    config.write_text("package_name_override: evilclient\npost_hooks: []\n")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "openapi_python_client",
            "generate",
            f"--path={spec}",
            f"--output-path={tmp_path / 'out'}",
            f"--custom-template-path={REPO / 'templates'}",
            f"--config={config}",
        ],
        check=True,
        capture_output=True,
    )

    sys.path.insert(0, str(tmp_path / "out"))
    try:
        thing = importlib.import_module("evilclient.models.thing")
        kind = importlib.import_module("evilclient.models.kind")
        parsed = thing.Thing.from_dict({"kind": "B"})
        assert parsed.kind is kind.Kind.B
    finally:
        sys.path.remove(str(tmp_path / "out"))
        for name in [m for m in sys.modules if m.startswith("evilclient")]:
            del sys.modules[name]

    assert not marker.exists(), "generated code executed a string from the spec"
