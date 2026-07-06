# WhatsApp Bridge auto-start
# Called by Task Scheduler at login. Waits for WSL filesystem to be ready,
# then runs the Go bridge. Task Scheduler owns the process lifetime.

$bridgeBin = "/mnt/c/Users/gabri/Projects/whatsapp-bridge/whatsapp-bridge/whatsapp-bridge"
$workDir   = "/mnt/c/Users/gabri"
$storeFile = "/mnt/c/Users/gabri/store/whatsapp.db"
$logFile   = "$env:TEMP\bridge.log"

# Directories send_file may read from (colon-separated). Setting
# WHATSAPP_MEDIA_ROOTS REPLACES the bridge's built-in default, so the
# default outbox and the store are listed explicitly alongside the
# Stagencies folder. Widening this list widens what a prompt-injected
# agent could exfiltrate via WhatsApp — keep it as narrow as practical.
$mediaRoots = "/home/gabriel/.local/share/whatsapp-mcp/outbox:/mnt/c/Users/gabri/store:/mnt/c/Users/gabri/OneDrive/Documents/Stagencies-Gabriel/Employers"

# Wake WSL immediately so it is warm before Claude Desktop tries to start MCP servers.
# WSL cold start takes 15-30s; doing this first wins the race against Claude Desktop's
# 60s MCP initialize timeout.
& "C:\Windows\System32\wsl.exe" bash -c "echo wsl-ready" | Out-Null

# Pre-warm the Python module cache in background, then stay resident.
# WSL ext4 cold boot takes 40-60s to import the MCP server's packages (VHDX
# reads via Windows I/O), racing Claude Desktop's 60s initialize timeout.
# The old one-shot subset-import warmup was unlogged and its effect did not
# survive until Claude Desktop spawned the server (2026-07-05 cold boot:
# import still took 40s, 13 minutes after login). warmhold.py imports the
# real server module (full dependency set), logs timings to
# %TEMP%\venv-warmup.log, and sleeps forever so the module pages stay mapped.
# The bash below waits for /mnt/c to be mounted, then replaces any holder
# left over from a previous session (the "$p" != "$$" guard keeps it from
# killing itself, since this command line also contains "warmhold.py").
Start-Job -ScriptBlock {
    & "C:\Windows\System32\wsl.exe" -e bash -c 'for i in $(seq 1 30); do [ -f /mnt/c/Users/gabri/Projects/whatsapp-bridge/whatsapp-mcp-server/warmhold.py ] && break; sleep 2; done; for p in $(pgrep -f warmhold.py); do [ "$p" != "$$" ] && kill "$p" 2>/dev/null; done; cd /mnt/c/Users/gabri/Projects/whatsapp-bridge/whatsapp-mcp-server && exec /home/gabriel/.whatsapp-mcp-venv/bin/python warmhold.py'
} | Out-Null

# Wait until the Windows filesystem is mounted and the store is accessible.
# /mnt/c can be missing for 10-30s after login on slow boots.
$maxWait = 60  # seconds
$waited  = 0
do {
    $ready = & "C:\Windows\System32\wsl.exe" bash -c "test -f $storeFile && echo yes || echo no" 2>$null
    if ($ready.Trim() -eq "yes") { break }
    Start-Sleep -Seconds 3
    $waited += 3
} while ($waited -lt $maxWait)

if ($ready.Trim() -ne "yes") {
    Add-Content -Path "$env:TEMP\whatsapp-bridge-start.log" -Value "$(Get-Date): Timed out waiting for store, aborting."
    exit 1
}

# Kill any stale instance from a previous session
& "C:\Windows\System32\wsl.exe" bash -c "pkill -f whatsapp-bridge 2>/dev/null; sleep 1"

# Restart loop — if the bridge exits for any reason, restart it after 5 seconds.
# Keeps the bridge alive through transient WhatsApp disconnects or crashes.
while ($true) {
    Add-Content -Path $logFile -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [autostart] starting bridge"
    & "C:\Windows\System32\wsl.exe" bash -c "cd $workDir && WHATSAPP_MEDIA_ROOTS='$mediaRoots' $bridgeBin 2>&1" >> $logFile
    $exitCode = $LASTEXITCODE
    Add-Content -Path $logFile -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [autostart] bridge exited (code $exitCode), restarting in 5s"
    Start-Sleep -Seconds 5
}
