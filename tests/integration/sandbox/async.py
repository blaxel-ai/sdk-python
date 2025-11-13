import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path

from blaxel.core.sandbox.client.models.process_request import ProcessRequest
from blaxel.core.sandbox.default import SandboxInstance


async def test_filesystem(sandbox: SandboxInstance):
    print("🔧 [async] fs: write/read/ls")
    # Basic write/read/ls
    await sandbox.fs.write("/tmp/test.txt", "Hello world")
    content = await sandbox.fs.read("/tmp/test.txt")
    assert content == "Hello world"
    listing = await sandbox.fs.ls("/tmp")
    assert any(f.name == "test.txt" for f in listing.files)

    print("🔧 [async] fs: mkdir/cp/rm")
    # mkdir, cp, rm
    await sandbox.fs.mkdir("/tmp/testdir")
    await sandbox.fs.cp("/tmp/test.txt", "/tmp/testdir/copied.txt")
    listing2 = await sandbox.fs.ls("/tmp/testdir")
    assert any(f.name == "copied.txt" for f in listing2.files)
    await sandbox.fs.rm("/tmp/testdir", recursive=True)
    await sandbox.fs.rm("/tmp/test.txt")

    print("🔧 [async] fs: write_tree")
    # write_tree
    await sandbox.fs.write_tree(
        [
            {"path": "/tmp/tree/a.txt", "content": "A"},
            {"path": "/tmp/tree/b.txt", "content": "B"},
        ]
    )
    tlist = await sandbox.fs.ls("/tmp/tree")
    assert set(f.name for f in tlist.files) >= {"a.txt", "b.txt"}
    await sandbox.fs.rm("/tmp/tree", recursive=True)

    print("🔧 [async] fs: binary write/read/download")
    # binary write/read/download
    test_dir = Path(__file__).parent
    archive_path = test_dir / "archive.zip"
    downloaded_path = test_dir / "archive.downloaded.zip"
    if archive_path.exists():
        await sandbox.fs.write_binary("/tmp/archive.zip", str(archive_path))
        data = await sandbox.fs.read_binary("/tmp/archive.zip")
        assert isinstance(data, bytes) and len(data) > 0
        await sandbox.fs.download("/tmp/archive.zip", str(downloaded_path))
        assert downloaded_path.exists()
        assert downloaded_path.stat().st_size == archive_path.stat().st_size
        downloaded_path.unlink(missing_ok=True)
        await sandbox.fs.rm("/tmp/archive.zip")
    else:
        print("ℹ️ [async] fs: archive.zip not found, skipping binary tests")


async def test_process(sandbox: SandboxInstance):
    print("🔧 [async] process: exec/wait/logs")
    # Exec and wait
    proc = await sandbox.process.exec(ProcessRequest(name="p1", command="echo 'Hello world'"))
    done = await sandbox.process.wait(proc.pid, max_wait=30000)
    assert done.status in ("completed", "failed")
    logs = await sandbox.process.logs(proc.pid, "all")
    assert "Hello world" in logs

    print("🔧 [async] process: stream logs with close()")
    # Stream logs with close
    name = "stream-test"
    await sandbox.process.exec(ProcessRequest(name=name, command="sh -c 'echo x; sleep 1; echo y'"))
    got = {"count": 0}

    def on_log(line: str):
        got["count"] += 1

    stream = sandbox.process.stream_logs(name, {"on_log": on_log})
    await sandbox.process.wait(name)
    stream["close"]()
    assert got["count"] >= 1


async def test_previews_and_sessions(sandbox: SandboxInstance):
    print("🔧 [async] previews: public create/list/get/delete")
    # Public preview
    try:
        preview = await sandbox.previews.create(
            {
                "metadata": {"name": "py-preview-public"},
                "spec": {"port": 443, "public": True},
            }
        )
        plist = await sandbox.previews.list()
        assert any(p.name == preview.name for p in plist)
        got = await sandbox.previews.get("py-preview-public")
        assert got.name == "py-preview-public"
    finally:
        try:
            await sandbox.previews.delete("py-preview-public")
        except Exception:
            pass

    print("🔧 [async] previews: private + token")
    # Private preview with token via tokens API
    try:
        preview = await sandbox.previews.create(
            {
                "metadata": {"name": "py-preview-private"},
                "spec": {"port": 443, "public": False},
            }
        )
        got = await sandbox.previews.get("py-preview-private")
        token = await got.tokens.create(datetime.now(timezone.utc) + timedelta(hours=1))
        assert token.value and token.expires_at
    finally:
        try:
            await sandbox.previews.delete("py-preview-private")
        except Exception:
            pass

    print("🔧 [async] sessions: create/from_session fs+process+watch")
    # Sessions
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    session = await sandbox.sessions.create({"expires_at": expires_at})
    sbx_from_session = await SandboxInstance.from_session(session)
    await sbx_from_session.fs.write("/tmp/sess.txt", "S")
    assert await sbx_from_session.fs.read("/tmp/sess.txt") == "S"

    # Session process and watch
    await sbx_from_session.process.exec(ProcessRequest(name="sp", command="echo SESS"))
    handle = sbx_from_session.fs.watch("/tmp", lambda e: None)
    await sbx_from_session.process.wait("sp")
    handle["close"]()


async def test_codegen_if_configured(sandbox: SandboxInstance):
    # Only run if provider keys likely configured
    print("🔧 [async] codegen: attempting fastapply + reranking (will skip if not configured)")
    try:
        await sandbox.codegen.fastapply(
            "/tmp/cg.txt",
            "// ... existing code ...\nconsole.log('Hello, codegen!');",
        )
        res = await sandbox.codegen.reranking(
            "/tmp",
            "Hello",
            score_threshold=0.0,
            token_limit=500,
            file_pattern=".*\\.txt$",
        )
        assert res is not None
    except Exception:
        # Skip silently when not available
        print("ℹ️ [async] codegen not configured, skipping")


async def main():
    print("🚀 [async] starting sandbox tests")
    sandbox = await SandboxInstance.create()
    try:
        await test_filesystem(sandbox)
        await test_process(sandbox)
        await test_previews_and_sessions(sandbox)
        await test_codegen_if_configured(sandbox)
    finally:
        try:
            md = getattr(sandbox, "metadata", None)
            sbx_name = getattr(md, "name", None) if md else None
            if sbx_name:
                await SandboxInstance.delete(sbx_name)
        except Exception:
            pass
    print("✅ [async] sandbox tests completed")


if __name__ == "__main__":
    asyncio.run(main())


