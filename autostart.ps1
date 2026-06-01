# WhatsApp Bridge auto-start
# Called by Task Scheduler at login. Waits for WSL filesystem to be ready,
# then runs the Go bridge. Task Scheduler owns the process lifetime.

$bridgeBin = "/mnt/c/Users/gabri/Projects/whatsapp-bridge/whatsapp-bridge/whatsapp-bridge"
$workDir   = "/mnt/c/Users/gabri"
$storeFile = "/mnt/c/Users/gabri/store/whatsapp.db"
$logFile   = "$env:TEMP\bridge.log"

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
    & "C:\Windows\System32\wsl.exe" bash -c "cd $workDir && $bridgeBin 2>&1" >> $logFile
    $exitCode = $LASTEXITCODE
    Add-Content -Path $logFile -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [autostart] bridge exited (code $exitCode), restarting in 5s"
    Start-Sleep -Seconds 5
}
