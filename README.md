# WebSocket Chat Application

A simple WebSocket-based chat application with message history persistence. The client automatically generates a unique ID and stores messages on the server, allowing users to retrieve their chat history when they reconnect.

## Features

- WebSocket real-time communication
- Message history stored on the server
- Simple, clean interface

## Project Structure

```
ChatBot/
├── server.py          # WebSocket server (Python)
├── client.html        # HTML interface
├── client.js          # Client-side WebSocket logic (javascript)
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Requirements

- Python 3.7+
- `websockets` library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/daniela-veloz/WebSocketChat.git
cd WebSocketChat
```

2. (Optional) Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Start the Server

```bash
python server.py
```

The server will start on `localhost:8765`.

### 2. Open the Client

Open `client.html` in your web browser:

```bash
open client.html
```

Or use Python's built-in HTTP server:
```bash
python -m http.server 8000
```
Then navigate to: `http://localhost:8000/client.html`

### 3. Start Chatting

- The client automatically connects to the server when the page loads
- Type your message in the input field and press Enter or click Send
- Your messages are stored on the server and will be available when you reconnect
- Each client is assigned a unique ID stored in localStorage

## How It Works

### Server Architecture

The server (`server.py`) uses two data structures:
- `active_connections`: A set tracking active WebSocket connections
- `message_history`: A dictionary mapping client IDs to their message lists

**Message Protocol:**
- `init`: Client sends client_id, server responds with message history
- `message`: Client sends message content, server stores it and sends acknowledgment
- `error`: Server sends error messages to client

### Client Architecture

The client (`client.js`) automatically:
1. Generates or retrieves a unique client ID from localStorage
2. Connects to the WebSocket server on page load
3. Receives and displays message history
4. Sends messages and displays them locally

## Configuration

You can modify the server configuration in `server.py`:

```python
HOST = "localhost"  # Server host
PORT = 8765         # Server port
```

## Technical Justification

### Why WebSocket?

WebSocket was chosen over HTTP/REST for the following reasons:

- **Full-duplex communication**: Enables real-time bidirectional messaging between client and server
- **Persistent connection**: Eliminates the overhead of establishing new connections for each message (unlike HTTP polling)
- **Low latency**: Messages are delivered instantly without polling delays
- **Efficient**: Reduces bandwidth usage compared to HTTP long-polling or Server-Sent Events
- **Native browser support**: Modern browsers support WebSocket natively without additional libraries

**Alternative considered**: HTTP with polling would be simpler but introduces latency and higher server load.

### Why In-Memory Storage?

The application uses Python dictionaries to store message history in memory:

- **Simplicity**: No database setup, configuration, or dependencies required
- **Performance**: Instant read/write operations with O(1) lookup time
- **Development speed**: Perfect for prototyping and learning WebSocket concepts
- **Minimal overhead**: No database connection management or query optimization needed

**Trade-offs**:
- Messages are lost when the server restarts
- No scalability across multiple server instances
- Limited by available RAM

**When to migrate**: For production use, replace with Redis (for speed) or PostgreSQL/MongoDB (for persistence and complex queries).

### Why This Message Protocol?

The JSON-based message protocol uses a simple `type` field to distinguish message kinds:

```javascript
// Init message
{ type: 'init', client_id: 'client_123' }

// Chat message
{ type: 'message', content: 'Hello world' }

// Error response
{ type: 'error', message: 'Invalid JSON format' }
```

**Rationale**:
- **Self-describing**: Each message contains its purpose, making debugging easier
- **Extensible**: Easy to add new message types without breaking existing functionality
- **JSON format**: Universal format supported by all programming languages and browsers
- **Type-based routing**: Server can easily dispatch messages based on `type` field

**Alternative considered**: Binary protocols (like Protocol Buffers) would be more efficient but add complexity and reduce readability for a simple chat app.

## Troubleshooting

**Error: "address already in use"**

If you get this error, another process is using port 8765. Find and kill it:
```bash
lsof -ti:8765 | xargs kill
```

Or change the `PORT` in `server.py` to a different value.
