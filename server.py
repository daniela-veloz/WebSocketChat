import asyncio
import json
from typing import Dict, Set, List

import websockets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
HOST = "localhost"
PORT = 8765

# Separate data structures for connections and message history
active_connections: Set[websockets.WebSocketServerProtocol] = set()
message_history: Dict[str, List[str]] = {}  # client_id -> list of messages

async def handle(websocket: websockets.WebSocketServerProtocol) -> None:
    active_connections.add(websocket)
    client_id = None
    logger.info(f"Client connected. Total connected clients: {len(active_connections)}")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)

                if data.get('type') == 'init':
                    client_id = data.get('client_id')
                    logger.info(f"Client {client_id} initialized.")

                    # send history
                    if client_id in message_history:
                        await websocket.send(json.dumps({
                            'type': 'history',
                            'messages': message_history[client_id]
                        }))
                    else:
                        message_history[client_id] = []

                elif data.get('type') == 'message' and client_id:
                    logger.info(f"Client {client_id} sent message: {data}")
                    message_history[client_id].append(data['content'])

                    # send ack response back to client
                    await websocket.send(json.dumps({
                        'type': 'message',
                        'message': 'ack'
                    }))

            except json.JSONDecodeError:
                logger.error(f"Client {client_id or 'unknown'} sent invalid JSON: {message}")
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': 'Invalid JSON format'
                }))
            except Exception as e:
                logger.error(f"Client {client_id or 'unknown'} error: {e}")
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': 'Internal server error'
                }))

    except websockets.exceptions.ConnectionClosedError:
        logger.info(f"Client {client_id or 'unknown'} connection closed.")
    except websockets.exceptions.ConnectionClosedOK:
        logger.info(f"Client {client_id or 'unknown'} disconnected cleanly.")
    except Exception as e:
        logger.error(f"Client {client_id or 'unknown'} unexpected error: {e}")
    finally:
        active_connections.discard(websocket)
        logger.info(f"Client {client_id or 'unknown'} disconnected. Total connected clients: {len(active_connections)}")

async def main() -> None:
    server = await websockets.serve(handle, HOST, PORT)
    logger.info(f"Server started on {HOST}:{PORT}")
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())




