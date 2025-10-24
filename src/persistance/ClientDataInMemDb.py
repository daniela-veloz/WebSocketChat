from typing import Dict, List

from persistance.ClientDataDb import ClientDataDb
from models.message import Message, MessageSender


class ClientDataInMemDb(ClientDataDb):
    """In-memory implementation of ClientDataDb."""

    def __init__(self):
        self.message_history: Dict[str, List[Message]] = {}  # client_id -> list of messages

    def add_client(self, client_id: str) -> None:
        self.validate_client_id(client_id)
        if client_id not in self.message_history:
            self.message_history[client_id] = []

    def add_message(self, client_id: str, sender: MessageSender, content: str) -> None:
        self.validate_client_id(client_id)
        if client_id not in self.message_history:
            raise ValueError(f"Client {client_id} does not exist. Call add_client first.")
        message = Message(sender=sender, content=content)
        self.message_history[client_id].append(message)

    def get_history(self, client_id: str) -> List[Message]:
        self.validate_client_id(client_id)
        if client_id not in self.message_history:
            raise ValueError(f"Client {client_id} does not exist")
        # Return a copy to prevent external modification
        return self.message_history[client_id].copy()

    def client_exists(self, client_id: str) -> bool:
        self.validate_client_id(client_id)
        return client_id in self.message_history
