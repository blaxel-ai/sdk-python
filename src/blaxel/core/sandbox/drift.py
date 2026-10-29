"""Tell the caller when create_if_not_exists returned a sandbox that is not the one asked for."""

import sys
from dataclasses import dataclass
from typing import Any, List

from ..client.models import Env, Sandbox
from ..client.types import UNSET

# The control plane masks every env value it reads back, so values can only be compared when it did not.
_MASKED_ENV_VALUE = "****"


def caller_stacklevel() -> int:
    """The stacklevel that makes a warning, raised by the function calling this one, point at the
    first frame outside the SDK: create_if_not_exists, create and the interpreter wrappers are all
    one call away from the code that actually passed the stale configuration.
    """
    frame = sys._getframe(1)
    level = 1
    while frame is not None and frame.f_globals.get("__name__", "").startswith("blaxel."):
        frame = frame.f_back  # type: ignore[assignment]
        level += 1
    return level


@dataclass(frozen=True)
class RequestedSandbox:
    """The fields of a create request that are compared with an existing sandbox.

    A field the caller did not set is None and is not compared.
    """

    image: str | None = None
    memory: int | None = None
    region: str | None = None
    envs: List[Env] | None = None


def _set(value: Any) -> Any:
    """The value, or None when the model leaves the field unset."""
    return None if value is UNSET else value


def requested_from_model(sandbox: Sandbox) -> RequestedSandbox:
    """What a Sandbox model asks for, read before the defaults fill the gaps."""
    spec = sandbox.spec or None
    runtime = (_set(spec.runtime) or None) if spec else None
    return RequestedSandbox(
        image=_set(runtime.image) if runtime else None,
        memory=_set(runtime.memory) if runtime else None,
        region=_set(spec.region) if spec else None,
        envs=_set(runtime.envs) if runtime else None,
    )


def _with_tag(image: str) -> str:
    # The control plane keeps the image reference as submitted: "app" and "app:latest" are the same image.
    if "@" in image:
        return image
    return image if ":" in image.rsplit("/", 1)[-1] else f"{image}:latest"


def _env_drift(requested: List[Env], existing: List[Env]) -> str | None:
    by_name = {env.name: env for env in existing}
    missing: List[str] = []
    changed: List[str] = []
    for env in requested:
        current = by_name.get(env.name)
        if current is None:
            missing.append(str(env.name))
        elif (
            current.value is not UNSET
            and current.value != _MASKED_ENV_VALUE
            and current.value != env.value
        ):
            changed.append(str(env.name))
    # Names only: env values are often secrets and never go into a log line.
    parts = []
    if missing:
        parts.append(f"not set on the existing sandbox: {', '.join(missing)}")
    if changed:
        parts.append(f"different value: {', '.join(changed)}")
    return f"envs ({'; '.join(parts)})" if parts else None


def describe_drift(requested: RequestedSandbox, existing: Sandbox) -> List[str]:
    """How an existing sandbox differs from the configuration that was asked for.

    One entry per field (image, memory, region, envs); empty when nothing differs.
    A field the existing sandbox does not report is not drift.
    """
    drift: List[str] = []
    spec = existing.spec or None
    runtime = (_set(spec.runtime) or None) if spec else None
    image = _set(runtime.image) if runtime else None
    memory = _set(runtime.memory) if runtime else None
    region = _set(spec.region) if spec else None
    envs = _set(runtime.envs) if runtime else None

    if requested.image and image and _with_tag(requested.image) != _with_tag(image):
        drift.append(f"image (requested {requested.image}, existing {image})")
    if requested.memory is not None and memory is not None and requested.memory != memory:
        drift.append(f"memory (requested {requested.memory} MB, existing {memory} MB)")
    if requested.region and region and requested.region != region:
        drift.append(f"region (requested {requested.region}, existing {region})")
    if requested.envs and envs is not None:
        env_drift = _env_drift(requested.envs, envs)
        if env_drift:
            drift.append(env_drift)
    return drift


def drift_message(requested: RequestedSandbox, existing: Sandbox) -> str | None:
    """The single warning create_if_not_exists logs, or None when the sandbox is the one asked for.

    Best-effort diagnostics: a comparison that fails must not fail the create.
    """
    try:
        drift = describe_drift(requested, existing)
        if not drift:
            return None
        name = _set(existing.metadata.name) if existing.metadata else None
        target = f'"{name}" ' if name else ""
        return (
            f"SandboxInstance.create_if_not_exists: sandbox {target}already exists, "
            "so it was returned as is and the requested configuration was not applied. "
            f"It differs on: {'; '.join(drift)}. "
            "Delete the sandbox and create it again to apply the new configuration."
        )
    except Exception:
        return None
