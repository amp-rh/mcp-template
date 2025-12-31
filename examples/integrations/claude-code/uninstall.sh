#!/bin/bash
# Uninstallation script for removing this MCP server from Claude Code

set -e

SERVER_NAME="${MCP_SERVER_NAME:-mcp-server}"

echo "🗑️  Uninstalling $SERVER_NAME from Claude Code..."
echo

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "❌ Error: Claude Code CLI not found"
    exit 1
fi

# Remove the server
if claude mcp get "$SERVER_NAME" &> /dev/null; then
    claude mcp remove "$SERVER_NAME"
    echo "✅ $SERVER_NAME removed successfully!"
else
    echo "⚠️  $SERVER_NAME not found in Claude Code configuration"
fi
echo
