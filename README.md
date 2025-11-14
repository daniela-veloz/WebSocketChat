# WebSocket Chat Application

A simple WebSocket-based chat application with message history persistence using SQLite. The client automatically generates a unique ID and stores messages on the server, allowing users to retrieve their chat history when they reconnect.

## Features

- WebSocket real-time communication
- Message history stored persistently in SQLite database
- Flask web server for serving the client interface
- Simple, clean interface
- Both in-memory and SQLite storage implementations available

## Project Structure

```
ChatBot/
├── main.py                            # Main entry point (runs both servers)
├── server.py                          # WebSocket server
├── web_server.py                      # Flask web server
├── client.html                        # HTML interface
├── client.js                          # Client-side WebSocket logic
├── requirements.txt                   # Python dependencies
├── models/
│   └── message.py                     # Message model with sender types
├── persistance/
│   ├── ClientDataDb.py                # Abstract database interface
│   ├── ClientDataInMemDb.py           # In-memory database implementation
│   └── ClientDataSqliteDb.py          # SQLite database implementation
└── README.md                          # This file
```

## Requirements

- Python 3.7+
- `websockets` library
- `flask` library

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

### 1. Start the Application

```bash
python main.py
```

This will start both:
- Flask web server on `http://localhost:5000`
- WebSocket server on `ws://localhost:8765`

### 2. Open the Client

Navigate to `http://localhost:5000` in your web browser.

### 3. Start Chatting

- The client automatically connects to the WebSocket server when the page loads
- Type your message in the input field and press Enter or click Send
- Your messages are stored persistently in a SQLite database (`webchat.db`)
- Messages will be available when you reconnect
- Each client is assigned a unique ID stored in localStorage

## How It Works

### Server Architecture

The application runs two servers concurrently:

1. **Flask Web Server** (`web_server.py`):
   - Serves static files (client.html, client.js)
   - Runs on port 5000
   - Handles HTTP requests

2. **WebSocket Server** (`server.py`):
   - Handles real-time bidirectional communication
   - Manages active connections
   - Persists messages to SQLite database
   - Runs on port 8765

**Message Protocol:**
- `init`: Client sends client_id, server responds with message history from database
- `message`: Client sends message content, server stores it in SQLite and sends acknowledgment
- `error`: Server sends error messages to client

### Database Architecture

The application uses a flexible storage system:
- `ClientDataDb`: Abstract interface for database operations
- `ClientDataSqliteDb`: SQLite implementation with persistent storage (default)
- `ClientDataInMemDb`: In-memory implementation for testing/development

SQLite schema:
- `clients` table: Stores client_id
- `messages` table: Stores messages with client_id, sender, content, and timestamp

### Client Architecture

The client (`client.js`) automatically:
1. Generates or retrieves a unique client ID from localStorage
2. Connects to the WebSocket server on page load
3. Receives and displays message history
4. Sends messages and displays them locally

## Configuration

You can modify the server configuration in `main.py`:

```python
# Flask web server
run_web_server(host='0.0.0.0', port=5000)

# WebSocket server
server = ChatServer(host="localhost", port=8765)
```

To switch between database implementations, edit `server.py`:

```python
# Use SQLite (persistent storage)
self.client_db = ClientDataSqliteDb()

# Or use in-memory storage
# self.client_db = ClientDataInMemDb()
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

### Why SQLite Storage?

The application uses SQLite for persistent message storage:

- **Persistent storage**: Messages survive server restarts
- **Zero configuration**: No separate database server needed
- **Lightweight**: Single file database, included in Python standard library
- **ACID compliance**: Reliable data integrity with transaction support
- **Performance**: Fast for single-user and small-scale applications
- **Portability**: Database is a single file that can be easily backed up

**Trade-offs**:
- Not suitable for high-concurrency scenarios (thousands of simultaneous writes)
- Limited scalability for distributed systems
- Single file can become large over time

**Alternative implementation available**: The codebase includes `ClientDataInMemDb` for in-memory storage, useful for testing or when persistence is not required.

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

If you get this error, another process is using port 8765 or 5000. Find and kill it:
```bash
# For WebSocket server (port 8765)
lsof -ti:8765 | xargs kill

# For Flask server (port 5000)
lsof -ti:5000 | xargs kill
```

Or change the ports in `main.py` to different values.

**Database locked error**

If you see SQLite database locked errors:
- Ensure only one instance of the server is running
- Check that no other process has the `webchat.db` file open
- The application uses `check_same_thread=False` to allow multi-threaded access

**WebSocket connection refused**

- Ensure both servers are running (check `main.py` output)
- Verify WebSocket URL in `client.js` matches your server configuration
- Check browser console for detailed error messages
