#!/bin/bash
# Restart loop for the MCP server in SSE mode (port 8000).
# Called from autostart.ps1 via nohup so it survives the parent process.
while true; do
    BRIDGE_TOKEN=$(cat /mnt/c/Users/gabri/store/.bridge-token 2>/dev/null)
    WHATSAPP_BRIDGE_TOKEN="$BRIDGE_TOKEN" \
    WHATSAPP_DB_PATH=/mnt/c/Users/gabri/store/messages.db \
    WHATSMEOW_DB_PATH=/mnt/c/Users/gabri/store/whatsapp.db \
    /home/gabriel/.local/bin/uv \
        --directory /mnt/c/Users/gabri/Projects/whatsapp-bridge/whatsapp-mcp-server \
        run python main.py sse
    sleep 5
done
