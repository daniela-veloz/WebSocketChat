import asyncio
import threading
from web_socket_server import WebSocketServer
from web_server import run_web_server


def start_flask_server():
    """Run Flask server in a separate thread."""
    print("Starting Flask web server on http://0.0.0.0:5001")
    run_web_server(host='0.0.0.0', port=5001)


async def start_websocket_server():
    """Run WebSocket server."""
    server = WebSocketServer(host="localhost", port=8765)
    await server.start()


async def main():
    """Start both Flask and WebSocket servers."""
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()

    # Start WebSocket server in the main asyncio event loop
    await start_websocket_server()


if __name__ == '__main__':
    print("Starting ChatBot application...")
    print("Web interface will be available at: http://localhost:5001")
    print("WebSocket server will run on: ws://localhost:8765")
    asyncio.run(main())