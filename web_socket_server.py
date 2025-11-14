import asyncio
import json
from typing import Set, Optional

import websockets
import logging

from models.message import MessageSender
from persistance.ClientDataSqliteDb import ClientDataSqliteDb


class WebSocketServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.active_connections: Set[websockets.WebSocketServerProtocol] = set()
        self.client_db = ClientDataSqliteDb()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def handle_client(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """
        Handle a client connection.
        """
        self.active_connections.add(websocket)
        client_id: Optional[str] = None
        self.logger.info(f"Client connected. Total connected clients: {len(self.active_connections)}")

        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get('type') == 'init':
                        client_id = await self._handle_init(websocket, data)

                    elif data.get('type') == 'message' and client_id:
                        await self._handle_message(websocket, client_id, data)

                except json.JSONDecodeError:
                    await self._send_error(websocket, client_id, "Invalid JSON format", message)
                except Exception as e:
                    await self._send_error(websocket, client_id, "Internal server error", str(e))

        except websockets.exceptions.ConnectionClosedError:
            self.logger.info(f"Client {client_id or 'unknown'} connection closed.")
        except websockets.exceptions.ConnectionClosedOK:
            self.logger.info(f"Client {client_id or 'unknown'} disconnected cleanly.")
        except Exception as e:
            self.logger.error(f"Client {client_id or 'unknown'} unexpected error: {e}")
        finally:
            self.active_connections.discard(websocket)
            self.logger.info(f"Client {client_id or 'unknown'} disconnected. Total connected clients: {len(self.active_connections)}")

    async def _handle_init(self, websocket: websockets.WebSocketServerProtocol, data: dict) -> Optional[str]:
        client_id = data.get('client_id')
        self.logger.info(f"Client {client_id} initialized.")

        if self.client_db.client_exists(client_id):
            self.logger.info(f"Client {client_id} reconnected.")
            # send history
            history = self.client_db.get_history(client_id)
            await websocket.send(json.dumps({
                'type': 'history',
                'messages': [msg.to_dict() for msg in history]
            }))
        else:
            self.client_db.add_client(client_id)

        return client_id

    async def _handle_message(self, websocket: websockets.WebSocketServerProtocol, client_id: str, data: dict) -> None:
        self.logger.info(f"Client {client_id} sent message: {data}")
        # Store user message with sender type
        self.client_db.add_message(client_id, MessageSender.USER, data['content'])
        self.client_db.add_message(client_id, MessageSender.SYSTEM, 'ack')

        # Send acknowledgment
        await websocket.send(json.dumps({
            'type': 'message',
            'message': 'ack'
        }))

    async def _send_error(self, websocket: websockets.WebSocketServerProtocol, client_id: Optional[str], error_message: str, details: str = "") -> None:
        self.logger.error(f"Client {client_id or 'unknown'} error: {details or error_message}")
        await websocket.send(json.dumps({
            'type': 'error',
            'message': error_message
        }))

    async def start(self) -> None:
        server = await websockets.serve(self.handle_client, self.host, self.port)
        self.logger.info(f"Server started on {self.host}:{self.port}")
        await server.wait_closed()


async def main() -> None:
    server = WebSocketServer(host="localhost", port=8765)
    await server.start()


if __name__ == '__main__':
    asyncio.run(main())




