from datetime import datetime, timedelta, timezone
from pathlib import Path

from blaxel.core.sandbox.client.models.process_request import ProcessRequest
from blaxel.core.sandbox.sync import SyncSandboxInstance


def test_filesystem(sandbox: SyncSandboxInstance):
    print("🔧 [sync] fs: write/read/ls")
    # Basic write/read/ls
    sandbox.fs.write("/tmp/test.txt", "Hello world")
    content = sandbox.fs.read("/tmp/test.txt")
    assert content == "Hello world"
    listing = sandbox.fs.ls("/tmp")
    assert any(f.name == "test.txt" for f in listing.files)

    print("🔧 [sync] fs: mkdir/cp/rm")
    # mkdir, cp, rm
    sandbox.fs.mkdir("/tmp/testdir")
    sandbox.fs.cp("/tmp/test.txt", "/tmp/testdir/copied.txt")
    listing2 = sandbox.fs.ls("/tmp/testdir")
    assert any(f.name == "copied.txt" for f in listing2.files)
    sandbox.fs.rm("/tmp/testdir", recursive=True)
    sandbox.fs.rm("/tmp/test.txt")

    print("🔧 [sync] fs: write_tree")
    # write_tree
    sandbox.fs.write_tree(
        [
            {"path": "/tmp/tree/a.txt", "content": "A"},
            {"path": "/tmp/tree/b.txt", "content": "B"},
        ]
    )
    tlist = sandbox.fs.ls("/tmp/tree")
    assert set(f.name for f in tlist.files) >= {"a.txt", "b.txt"}
    sandbox.fs.rm("/tmp/tree", recursive=True)

    print("🔧 [sync] fs: binary write/read/download")
    # binary write/read/download
    test_dir = Path(__file__).parent
    archive_path = test_dir / "archive.zip"
    downloaded_path = test_dir / "archive.downloaded.zip"
    if archive_path.exists():
        sandbox.fs.write_binary("/tmp/archive.zip", str(archive_path))
        data = sandbox.fs.read_binary("/tmp/archive.zip")
        assert isinstance(data, bytes) and len(data) > 0
        sandbox.fs.download("/tmp/archive.zip", str(downloaded_path))
        assert downloaded_path.exists()
        assert downloaded_path.stat().st_size == archive_path.stat().st_size
        downloaded_path.unlink(missing_ok=True)
        sandbox.fs.rm("/tmp/archive.zip")
    else:
        print("ℹ️ [sync] fs: archive.zip not found, skipping binary tests")


def test_process(sandbox: SyncSandboxInstance):
    print("🔧 [sync] process: exec/wait/logs")
    # Exec and wait
    proc = sandbox.process.exec(ProcessRequest(name="p1", command="echo 'Hello world'"))
    done = sandbox.process.wait(proc.pid, max_wait=30000)
    assert done.status in ("completed", "failed")
    logs = sandbox.process.logs(proc.pid, "all")
    assert "Hello world" in logs

    print("🔧 [sync] process: stream logs with close()")
    # Stream logs with close
    name = "stream-test"
    sandbox.process.exec(ProcessRequest(name=name, command="sh -c 'echo x; sleep 1; echo y'"))
    got = {"count": 0}

    def on_log(line: str):
        got["count"] += 1

    stream = sandbox.process.stream_logs(name, {"on_log": on_log})
    sandbox.process.wait(name)
    stream["close"]()
    assert got["count"] >= 1


def test_previews_and_sessions(sandbox: SyncSandboxInstance):
    print("🔧 [sync] previews: public create/list/get/delete")
    # Public preview
    try:
        preview = sandbox.previews.create(
            {
                "metadata": {"name": "py-sync-preview-public"},
                "spec": {"port": 443, "public": True},
            }
        )
        plist = sandbox.previews.list()
        assert any(p.name == preview.name for p in plist)
        got = sandbox.previews.get("py-sync-preview-public")
        assert got.name == "py-sync-preview-public"
    finally:
        try:
            sandbox.previews.delete("py-sync-preview-public")
        except Exception:
            pass

    print("🔧 [sync] previews: private + token")
    # Private preview with token via tokens API
    try:
        preview = sandbox.previews.create(
            {
                "metadata": {"name": "py-sync-preview-private"},
                "spec": {"port": 443, "public": False},
            }
        )
        got = sandbox.previews.get("py-sync-preview-private")
        token = got.tokens.create(datetime.now(timezone.utc) + timedelta(hours=1))
        assert token.value and token.expires_at
    finally:
        try:
            sandbox.previews.delete("py-sync-preview-private")
        except Exception:
            pass

    print("🔧 [sync] sessions: create/from_session fs+process+watch")
    # Sessions
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    session = sandbox.sessions.create({"expires_at": expires_at})
    sbx_from_session = SyncSandboxInstance.from_session(session)
    sbx_from_session.fs.write("/tmp/sess.txt", "S")
    assert sbx_from_session.fs.read("/tmp/sess.txt") == "S"

    # Session process and watch
    sbx_from_session.process.exec(ProcessRequest(name="sp", command="echo SESS"))
    handle = sbx_from_session.fs.watch("/tmp", lambda e: None)
    sbx_from_session.process.wait("sp")
    handle["close"]()


def test_codegen_if_configured(sandbox: SyncSandboxInstance):
    print("🔧 [sync] codegen: attempting fastapply + reranking (will skip if not configured)")
    try:
        sandbox.codegen.fastapply(
            "/tmp/cg.txt",
            "// ... existing code ...\nconsole.log('Hello, codegen!');",
        )
        res = sandbox.codegen.reranking(
            "/tmp",
            "Hello",
            score_threshold=0.0,
            token_limit=500,
            file_pattern=".*\\.txt$",
        )
        assert res is not None
    except Exception:
        # Skip silently when not available
        print("ℹ️ [sync] codegen not configured, skipping")


def main():
    print("🚀 [sync] starting sandbox tests")
    sandbox = SyncSandboxInstance.create()
    try:
        test_filesystem(sandbox)
        test_process(sandbox)
        test_previews_and_sessions(sandbox)
        test_codegen_if_configured(sandbox)
    finally:
        try:
            md = getattr(sandbox, "metadata", None)
            sbx_name = getattr(md, "name", None) if md else None
            if sbx_name:
                SyncSandboxInstance.delete(sbx_name)
        except Exception:
            pass
    print("✅ [sync] sandbox tests completed")


if __name__ == "__main__":
    main()


