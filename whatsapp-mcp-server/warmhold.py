"""Pre-warm and keep warm the WhatsApp MCP server's module files.

Launched by autostart.ps1 at login (see repo root). Cold imports from the
WSL VHDX take 40-60s, which races Claude Desktop's 60s MCP initialize
timeout. Importing the real server module here pays that cost once, right
after login.

Holding the modules in this process is not enough: each server spawn is a
fresh python that re-reads every module file from disk, and the WSL VM's
small page cache evicts those files within hours of normal use (observed
2026-07-14: import cold again 2h after boot, and again 20 minutes after a
successful start). So after the initial import this process re-reads all
loaded module files (source + bytecode cache) every REWARM_INTERVAL
seconds — milliseconds when the cache is warm, one logged slow pass when
it had been evicted.

Every run appends to %TEMP%\\venv-warmup.log on the Windows side so a
failed or slow warmup is diagnosable after the fact.
"""

import importlib.util
import os
import sys
import time

LOG = "/mnt/c/Users/gabri/AppData/Local/Temp/venv-warmup.log"
REWARM_INTERVAL = 300  # seconds between page-cache refresh passes
SLOW_REWARM = 1.0  # log a pass only when it took this long (cache was evicted)


def log(msg: str) -> None:
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")


def module_files() -> list[str]:
    """Files a fresh interpreter reads to import everything currently loaded.

    For pure-python modules that is the .py source plus its compiled .pyc
    (the bytecode cache is what actually gets executed); C extensions just
    have their shared object.
    """
    files = []
    for mod in list(sys.modules.values()):
        path = getattr(mod, "__file__", None)
        if not path:
            continue
        files.append(path)
        if path.endswith(".py"):
            pyc = importlib.util.cache_from_source(path)
            if os.path.exists(pyc):
                files.append(pyc)
    return files


def rewarm(paths: list[str]) -> tuple[int, int]:
    """Read every file fully to pull its pages back into the page cache.

    Returns (files read, total bytes). Missing/unreadable files are skipped —
    the set can go stale after a pip upgrade, and the next login rebuilds it.
    """
    read = 0
    total = 0
    for path in paths:
        try:
            with open(path, "rb") as fh:
                while chunk := fh.read(1 << 20):
                    total += len(chunk)
            read += 1
        except OSError:
            continue
    return read, total


def run() -> None:
    log("warmup start")
    t0 = time.time()
    try:
        import main  # noqa: F401  (side effect: loads the full server dependency tree)
    except Exception as exc:
        log(f"warmup FAILED after {time.time() - t0:.1f}s: {exc!r}")
        raise
    log(f"warmup imported main in {time.time() - t0:.1f}s")

    paths = module_files()
    read, total = rewarm(paths)
    log(f"rewarm loop: {read} files, {total / 1e6:.1f} MB every {REWARM_INTERVAL}s")

    while True:
        time.sleep(REWARM_INTERVAL)
        t0 = time.time()
        read, total = rewarm(paths)
        elapsed = time.time() - t0
        if elapsed >= SLOW_REWARM:
            log(f"rewarmed {read} files ({total / 1e6:.1f} MB) in {elapsed:.1f}s — cache had been evicted")


if __name__ == "__main__":
    run()
