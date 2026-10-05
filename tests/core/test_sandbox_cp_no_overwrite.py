"""Opt-in copy protocol and the exact Linux shell used by async/sync wrappers."""

import inspect
import os
import shlex
import socket
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from blaxel.core.sandbox._copy_no_overwrite import (
    _COPY_NO_OVERWRITE_MARKER as MARKER,
)
from blaxel.core.sandbox._copy_no_overwrite import (
    _COPY_NO_OVERWRITE_SCRIPT as SCRIPT,
)
from blaxel.core.sandbox._copy_no_overwrite import _copy_no_overwrite_command
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem


async def call(fn, *args, **kwargs):
    result = fn(*args, **kwargs)
    return await result if inspect.isawaitable(result) else result


@pytest.fixture(params=[SandboxFileSystem, SyncSandboxFileSystem], ids=["async", "sync"])
def lane(request):
    cls = request.param
    fs = object.__new__(cls)
    mock = AsyncMock if cls is SandboxFileSystem else Mock
    execute = mock(return_value=SimpleNamespace(pid="pid-1"))
    wait = mock(return_value=SimpleNamespace(status="completed", exit_code=0, logs=""))
    fs.process = SimpleNamespace(exec=execute, wait=wait)
    return SimpleNamespace(fs=fs, execute=execute, wait=wait)


@pytest.mark.parametrize("kwargs", [{}, {"no_overwrite": False}])
async def test_default_branch_byte_for_byte(lane, kwargs):
    source, destination = "source ' ; $(touch BAD)", "destination\nユニコード"
    response = await call(lane.fs.cp, source, destination, **kwargs)
    assert response.__dict__ == {
        "message": "Files copied",
        "source": source,
        "destination": destination,
    }
    lane.execute.assert_called_once_with(
        {"command": f"cp -r {shlex.quote(source)} {shlex.quote(destination)}"}
    )
    lane.wait.assert_called_once_with("pid-1", max_wait=180000, interval=100)


async def test_default_failure_unchanged_and_positional_max_wait(lane):
    lane.wait.return_value = SimpleNamespace(status="failed", exit_code=73, logs=MARKER + "\n")
    with pytest.raises(Exception) as caught:
        await call(lane.fs.cp, "src", "dst", 123)
    assert type(caught.value) is Exception
    assert str(caught.value) == f"Could not copy src to dst cause: {MARKER}\n"
    lane.execute.assert_called_once_with({"command": "cp -r src dst"})
    lane.wait.assert_called_once_with("pid-1", max_wait=123, interval=100)


async def test_protected_quoting_wait_and_original_response(lane):
    source, destination = "-source ' ; $(touch BAD)\nユニコード", "-destination ' ; touch BAD\n"
    result = await call(lane.fs.cp, source, destination, 321, no_overwrite=True)
    command = lane.execute.call_args.args[0]["command"]
    assert shlex.split(command) == ["sh", "-c", SCRIPT, "sh", source, destination]
    lane.wait.assert_called_once_with("pid-1", max_wait=321, interval=100)
    assert result.__dict__ == {
        "message": "Files copied",
        "source": source,
        "destination": destination,
    }
    assert command == _copy_no_overwrite_command(source, destination)


async def test_no_overwrite_is_keyword_only(lane):
    with pytest.raises(TypeError):
        await call(lane.fs.cp, "src", "dst", 321, True)
    lane.execute.assert_not_called()


@pytest.mark.parametrize(
    "source,destination", [("", "dst"), ("src", ""), ("a\0b", "dst"), ("src", "a\0b")]
)
async def test_protected_validation_before_exec(lane, source, destination):
    with pytest.raises(
        ValueError, match="source and destination must be nonempty paths without NUL bytes"
    ):
        await call(lane.fs.cp, source, destination, no_overwrite=True)
    lane.execute.assert_not_called()
    lane.wait.assert_not_called()


@pytest.mark.parametrize("logs", [MARKER + "\n", "diagnostic\n" + MARKER + "\n", MARKER + "\r\n"])
async def test_exact_conflict_protocol(lane, logs):
    lane.wait.return_value = SimpleNamespace(status="failed", exit_code=73, logs=logs)
    with pytest.raises(FileExistsError) as caught:
        await call(lane.fs.cp, "original-source", "container", no_overwrite=True)
    assert (
        str(caught.value)
        == "Could not copy original-source to container: destination already exists"
    )
    assert caught.value.errno is None and caught.value.filename is None
    lane.execute.assert_called_once()
    lane.wait.assert_called_once_with("pid-1", max_wait=180000, interval=100)


@pytest.mark.parametrize(
    "status,exit_code,logs",
    [
        ("failed", 73, "File exists"),
        ("failed", 73, "prefix " + MARKER + "\n"),
        ("failed", 73, MARKER + " suffix\n"),
        ("failed", 1, MARKER + "\n"),
        ("failed", 1, "Permission denied"),
        ("failed", 1, "Missing parent"),
        ("completed", 73, MARKER + "\n"),
        ("running", 0, "pending"),
        ("unknown", 0, "unknown"),
        ("killed", 0, "killed"),
        ("stopped", 0, "stopped"),
        ("completed", None, "missing exit code"),
    ],
)
async def test_generic_failure_and_no_false_success(lane, status, exit_code, logs):
    lane.wait.return_value = SimpleNamespace(status=status, exit_code=exit_code, logs=logs)
    with pytest.raises(Exception) as caught:
        await call(lane.fs.cp, "src", "dst", no_overwrite=True)
    assert type(caught.value) is Exception
    assert str(caught.value) == f"Could not copy src to dst cause: {logs}"
    lane.execute.assert_called_once()
    lane.wait.assert_called_once()


@pytest.mark.parametrize("logs", [None, {}, 73])
async def test_unusable_logs_fail_generically(lane, logs):
    lane.wait.return_value = SimpleNamespace(status="failed", exit_code=73, logs=logs)
    with pytest.raises(Exception) as caught:
        await call(lane.fs.cp, "src", "dst", no_overwrite=True)
    assert type(caught.value) is Exception
    assert str(caught.value) == f"Could not copy src to dst cause: {logs}"


async def test_absent_logs_fail_generically(lane):
    lane.wait.return_value = SimpleNamespace(status="failed", exit_code=73)
    with pytest.raises(Exception) as caught:
        await call(lane.fs.cp, "src", "dst", no_overwrite=True)
    assert type(caught.value) is Exception
    assert str(caught.value) == "Could not copy src to dst cause: Unknown error"


@pytest.mark.parametrize("phase", ["exec", "wait"])
@pytest.mark.parametrize("failure", [RuntimeError("transport error"), TimeoutError("wait timeout")])
async def test_transport_and_timeout_propagate_without_retry_or_cleanup(lane, phase, failure):
    (lane.execute if phase == "exec" else lane.wait).side_effect = failure
    with pytest.raises(type(failure)) as caught:
        await call(lane.fs.cp, "src", "dst", no_overwrite=True)
    assert caught.value is failure
    assert lane.execute.call_count == 1
    assert lane.wait.call_count == (0 if phase == "exec" else 1)


def test_top_level_socket_rejected_before_reservation():
    # AF_UNIX paths have a short platform limit; pytest's macOS tmp_path is too long.
    with tempfile.TemporaryDirectory(dir="/tmp") as directory:
        source, destination = Path(directory) / "socket", Path(directory) / "target"
        with socket.socket(socket.AF_UNIX) as sock:
            sock.bind(str(source))
            result = subprocess.run(
                ["sh", "-c", _copy_no_overwrite_command(str(source), str(destination))],
                capture_output=True,
                text=True,
                timeout=5,
            )
        assert result.returncode == 1
        assert MARKER not in result.stderr.splitlines()
        assert not destination.exists()


DOCKER_IMAGE = os.environ.get("CP_NO_OVERWRITE_DOCKER_IMAGE")


@pytest.mark.skipif(
    not DOCKER_IMAGE and (sys.platform != "linux" or os.getuid() == 0),
    reason="requires non-root Linux or CP_NO_OVERWRITE_DOCKER_IMAGE",
)
def test_linux_shell_matrix():
    # Colima mounts the checkout, not macOS /var/folders tmp directories.
    with tempfile.TemporaryDirectory(
        prefix=".cp-no-overwrite-", dir=Path.cwd() if DOCKER_IMAGE else None
    ) as directory:
        root = Path(directory)
        root.chmod(0o755)
        (root / "copy.sh").write_text(SCRIPT)
        (root / "matrix.sh").write_text(_PLATFORM_MATRIX)
        command = (
            [
                "docker",
                "run",
                "--rm",
                "--user",
                "65534:65534",
                "-v",
                f"{root}:/spec:ro",
                DOCKER_IMAGE,
                "sh",
                "/spec/matrix.sh",
                "/spec/copy.sh",
            ]
            if DOCKER_IMAGE
            else ["sh", str(root / "matrix.sh"), str(root / "copy.sh")]
        )
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "PASS" in result.stdout
        assert result.stdout.count("winners=1 conflicts=23") == 4
        print(result.stdout)


# The same matrix as the TypeScript counterpart, including stable-target races.
_PLATFORM_MATRIX = r"""#!/bin/sh
set -eu
copy_script=$1
d=$(mktemp -d)
trap 'rm -rf "$d"' EXIT
cd "$d"
cpn() { sh "$copy_script" "$1" "$2"; }
blocked() {
  set +e
  cpn "$1" "$2" > log 2>&1
  status=$?
  set -e
  test "$status" = 73
  grep -qx 'BLAXEL_CP_NO_OVERWRITE_EXISTS' log
}
printf '%s' new > src
printf '%s' old > existing
blocked src existing
test "$(cat existing)" = old
ln -s missing dangling
blocked src dangling
test -L dangling
mkdir container
cpn src container
test "$(cat container/src)" = new
blocked src container
mkdir tree
printf hidden > tree/.hidden
mkdir tree/sub
printf data > tree/sub/a
ln -s sub/a tree/link
cpn tree container
test "$(cat container/tree/.hidden)" = hidden
test "$(cat container/tree/sub/a)" = data
test -L container/tree/link
blocked tree container
cpn tree fresh-tree
test -f fresh-tree/sub/a
test ! -e fresh-tree/tree
ln -s 'a b' src-link
cpn src-link link-copy
test "$(readlink link-copy)" = 'a b'
ln -s 'directory' link-as-file
blocked src link-as-file
ln -s container directory-link
blocked src directory-link
mkdir -p link-container/src-link
blocked src-link link-container
test ! -e link-container/src-link/'a b'
link_value=$(printf 'trailing\n\n.')
link_value=${link_value%.}
ln -s "$link_value" newline-link
cpn newline-link newline-copy
test "$(readlink newline-link && printf '.')" = "$(readlink newline-copy && printf '.')"
chmod 751 src
umask 027
cpn src mode-file
test "$(stat -c %a mode-file)" = 750
printf special > "./--input 'quoted' ; touch BAD"
cpn "./--input 'quoted' ; touch BAD" "./--output 'quoted' ; touch BAD"
test ! -e BAD
test "$(cat "./--output 'quoted' ; touch BAD")" = special
printf nl > "$(printf 'newline\nfile')"
cpn "$(printf 'newline\nfile')" "$(printf 'newline\ncopy')"
test "$(cat "$(printf 'newline\ncopy')")" = nl
tail_name=$(printf 'name-tail\n.')
tail_name=${tail_name%.}
printf tail > "$tail_name"
mkdir tail-container
cpn "$tail_name" tail-container
test "$(cat "tail-container/$tail_name")" = tail
set +e
cpn src missing-parent/target > log 2>&1; status=$?
set -e
test "$status" = 1
! grep -qx BLAXEL_CP_NO_OVERWRITE_EXISTS log
test ! -e missing-parent
set +e
cpn absent absent-target > log 2>&1; status=$?
set -e
test "$status" = 1
test ! -e absent-target
mkfifo fifo
set +e
cpn fifo fifo-target > log 2>&1; status=$?
set -e
test "$status" = 1
test ! -e fifo-target
# Stable effective paths, no removals: exactly one winner of 24 contenders.
# Directory contenders must use a pre-existing destination container: a newly
# created raw destination directory becomes a cp container for later calls.
mkdir race-directory-container
for type in file directory link; do
  destination="race-$type"
  case "$type" in file) source=src;; directory) source=tree; destination=race-directory-container;; link) source=src-link;; esac
  i=0
  while test "$i" -lt 24; do
    (set +e; cpn "$source" "$destination" > "race-$type-$i.log" 2>&1; printf '%s\n' "$?" > "race-$type-$i.status") &
    i=$((i+1))
  done
  wait
  winners=0
  conflicts=0
  for statusfile in race-"$type"-*.status; do
    status=$(cat "$statusfile")
    case "$status" in 0) winners=$((winners+1));; 73) conflicts=$((conflicts+1));; *) printf 'unexpected status %s\n' "$status"; exit 1;; esac
  done
  test "$winners" = 1
  test "$conflicts" = 23
  printf 'race %s: winners=%s conflicts=%s\n' "$type" "$winners" "$conflicts"
done
printf 'PASS: conflicts, effective directory targets, recursive content, symlinks, modes, quoting, missing parents/sources, FIFO rejection\n'

# Additional implementation acceptance coverage beyond the feasibility probe.
generic() {
  set +e
  cpn "$1" "$2" > log 2>&1
  status=$?
  set -e
  test "$status" = 1
  ! grep -qx BLAXEL_CP_NO_OVERWRITE_EXISTS log
}
blocked src src
ln src hard-alias
blocked src hard-alias
test "$(cat src)" = new
ln -s src file-alias
blocked src file-alias
test "$(readlink file-alias)" = src
mkdir untouched-root
printf original > untouched-root/keep
blocked tree/. untouched-root
test "$(cat untouched-root/keep)" = original
test ! -e untouched-root/.hidden
blocked . untouched-root
blocked .. untouched-root
blocked tree/ container
cpn tree/. dot-tree
test -f dot-tree/sub/a
test ! -e dot-tree/tree
mkdir trailing-container
cpn tree/ trailing-container
test -f trailing-container/tree/sub/a
ln -s tree directory-source-link
mkdir followed-container
cpn directory-source-link/ followed-container
test -d followed-container/directory-source-link
test ! -L followed-container/directory-source-link
test -f followed-container/directory-source-link/sub/a
generic src absent-slash/
test ! -e absent-slash
ln -s nonexistent dangling-parent
generic src dangling-parent/child
test ! -e dangling-parent/child
mkdir locked
chmod 555 locked
generic src locked/child
chmod 755 locked
generic /dev/null device-target
test ! -e device-target

# Ordinary rwx matches new-file cp-r, but protected copies strip special bits.
cp -r src reference-mode
cpn src protected-mode
test "$(stat -c %a reference-mode)" = "$(stat -c %a protected-mode)"
chmod 6751 src
cpn src no-special-bits
test "$(stat -c %a no-special-bits)" = 750

# The reserved directory root must not broaden a private source's permissions.
mkdir -m 700 private-directory
printf private > private-directory/file
cp -r private-directory reference-directory
cpn private-directory protected-directory
test "$(stat -c %a protected-directory)" = 700
test "$(stat -c %a protected-directory)" = "$(stat -c %a reference-directory)"
test "$(cat protected-directory/file)" = private

# Insert a symlink after the pre-check and before the file redirect claim.
# Noclobber can open a device/FIFO; the post-claim check must prevent cp.
mkdir claim-race-bin
printf '#!/bin/sh\n"%s" -s -- "$RACE_LINK_VALUE" "$RACE_LINK" || exit 1\nexec "%s" "$@"\n' "$(command -v ln)" "$(command -v stat)" > claim-race-bin/stat
chmod 755 claim-race-bin/stat
RACE_LINK="$d/late-device-link" RACE_LINK_VALUE=/dev/null PATH="$d/claim-race-bin:$PATH" blocked src late-device-link
test -L late-device-link
test "$(readlink late-device-link)" = /dev/null
# A reader allows the FIFO open to return. Without a reader, the claim can block.
mkfifo claim-fifo
cat claim-fifo > claim-fifo-read &
reader=$!
RACE_LINK="$d/late-fifo-link" RACE_LINK_VALUE="$d/claim-fifo" PATH="$d/claim-race-bin:$PATH" blocked src late-fifo-link
wait "$reader"
test -L late-fifo-link
test ! -s claim-fifo-read
printf 'PASS: directory root mode, post-claim device/FIFO symlink conflicts\n'

# Missing required utilities fail before creating an unprotected target.
set +e
PATH=/nonexistent /bin/sh "$copy_script" src no-tools > log 2>&1
status=$?
set -e
test "$status" = 1
test ! -e no-tools

# A utility's exit73 and arbitrary marker logs cannot impersonate a conflict.
mkdir fakebin
printf '#!/bin/sh\nprintf "BLAXEL_CP_NO_OVERWRITE_EXISTS\\n" >&2\nexit 73\n' > fakebin/cp
chmod 755 fakebin/cp
set +e
PATH="$d/fakebin:$PATH" cpn src partial-file > log 2>&1
status=$?
set -e
test "$status" = 1
test -f partial-file
test ! -s partial-file
blocked src partial-file
set +e
PATH="$d/fakebin:$PATH" cpn src existing > log 2>&1
status=$?
set -e
test "$status" = 73
test "$(cat existing)" = old
mkdir partial-container
set +e
PATH="$d/fakebin:$PATH" cpn tree partial-container > log 2>&1
status=$?
set -e
test "$status" = 1
test -d partial-container/tree
test ! -e partial-container/tree/.hidden
blocked tree partial-container

# Deterministically create a directory after the initial check but before ln.
# ln -s without mandatory -T would silently create a child and report success.
printf '#!/bin/sh\n"%s" "$@" || exit 1\n"%s" -- "$CLAIM_RACE_TARGET" || exit 1\n' "$(command -v readlink)" "$(command -v mkdir)" > fakebin/readlink
chmod 755 fakebin/readlink
set +e
CLAIM_RACE_TARGET="$d/late-directory" PATH="$d/fakebin:$PATH" cpn src-link late-directory > log 2>&1
status=$?
set -e
test "$status" = 73
test -d late-directory
test ! -L 'late-directory/a b'
mkdir late-real-directory
printf '#!/bin/sh\n"%s" "$@" || exit 1\n"%s" -s -- "$LATE_CONTAINER" "$CLAIM_RACE_TARGET" || exit 1\n' "$(command -v readlink)" "$(command -v ln)" > fakebin/readlink
set +e
LATE_CONTAINER="$d/late-real-directory" CLAIM_RACE_TARGET="$d/late-directory-link" PATH="$d/fakebin:$PATH" cpn src-link late-directory-link > log 2>&1
status=$?
set -e
test "$status" = 73
test -L late-directory-link
test ! -L 'late-real-directory/a b'

# Mixed source types claim exactly the same stable entry; ln -T must not nest.
mkdir mixed-container
i=0
while test "$i" -lt 24; do
  mkdir "mixed-$i"
  case "$((i % 3))" in
    0) printf mixed > "mixed-$i/same";;
    1) mkdir "mixed-$i/same"; printf hidden > "mixed-$i/same/.hidden";;
    2) ln -s do-not-nest "mixed-$i/same";;
  esac
  (set +e; cpn "mixed-$i/same" mixed-container > "mixed-$i.log" 2>&1; printf '%s\n' "$?" > "mixed-$i.status") &
  i=$((i+1))
done
wait
winners=0
conflicts=0
for statusfile in mixed-*.status; do
  status=$(cat "$statusfile")
  case "$status" in 0) winners=$((winners+1));; 73) conflicts=$((conflicts+1));; *) exit 1;; esac
done
test "$winners" = 1
test "$conflicts" = 23
test ! -e mixed-container/same/do-not-nest
printf 'race mixed: winners=%s conflicts=%s\n' "$winners" "$conflicts"
printf 'PASS: aliases, dot/trailing-slash paths, mode safety, missing tools, partial retention, mixed race\n'
"""
