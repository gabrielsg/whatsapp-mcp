"""Pre-warm and hold the WhatsApp MCP server's Python module cache.

Launched by autostart.ps1 at login (see repo root). Cold-boot imports from
the WSL VHDX take 40-60s, which races Claude Desktop's 60s MCP initialize
timeout. Importing the real server module here pays that cost once, right
after login. Staying resident afterwards keeps the module file pages mapped
so they are not evicted before Claude Desktop spawns the actual server —
which can be many minutes after login.

Every run appends to %TEMP%\\venv-warmup.log on the Windows side so a failed
or slow warmup is diagnosable after the fact (the previous subset-import
warmup was silent, so the 2026-07-05 cold-boot failure left no evidence).
"""

import time

LOG = "/mnt/c/Users/gabri/AppData/Local/Temp/venv-warmup.log"


def log(msg: str) -> None:
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")


log("warmup start")
t0 = time.time()
try:
    import main  # noqa: F401  (side effect: loads the full server dependency tree)
except Exception as exc:
    log(f"warmup FAILED after {time.time() - t0:.1f}s: {exc!r}")
    raise
log(f"warmup imported main in {time.time() - t0:.1f}s; holding resident")

while True:
    time.sleep(3600)
