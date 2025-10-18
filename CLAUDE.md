# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a WebSocket-based chat server application built with Python and the `websockets` library. The server maintains client connections and message history, allowing clients to reconnect and retrieve their previous messages.

## Architecture

**Server Architecture** (`server.py`):
- Uses `asyncio` and `websockets` for handling concurrent client connections
- `connected_clients` dictionary (line 11): Maps client IDs to their message history. Note: There's a bug where it's commented as "list of messages" but initialized as `{}` (dict), then used with `.add()` (set method) on line 14
- Message flow:
  - Client sends `init` message with `client_id` → server sends message history if available
  - Client sends `message` → server appends to history and sends acknowledgment
- Connection lifecycle managed in `handle()` function (lines 13-54)

## Development Commands

**Run the server**:
```bash
python server.py
```
The server runs on `localhost:8765` by default.

**Virtual environment**:
```bash
source .venv/bin/activate  # Activate venv
deactivate                  # Deactivate venv
```

**Dependencies**:
The project uses a virtual environment (`.venv/`) with:
- `websockets` (15.0.1) - WebSocket server implementation

To install dependencies:
```bash
pip install websockets
```

## Known Issues

There's a data structure inconsistency in `server.py`:
- Line 11: `connected_clients` initialized as `{}` (dict)
- Line 14: Used as `.add(websocket)` (set method)
- Line 28-34: Used as dict with client_id keys

This will cause runtime errors and needs to be fixed to use two separate data structures: one for active websocket connections (set) and one for message history (dict).