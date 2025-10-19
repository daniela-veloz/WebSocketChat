from abc import ABC, abstractmethod
from typing import List

from src.models.message import Message, MessageSender


class ClientDataDb(ABC):

    @staticmethod
    def validate_client_id(client_id: str) -> None:
        if client_id is None:
            raise ValueError("client_id cannot be None")
        if not isinstance(client_id, str):
            raise ValueError("client_id must be a string")
        if not client_id.strip():
            raise ValueError("client_id cannot be empty or whitespace")

    @abstractmethod
    def add_client(self, client_id: str) -> None:
        pass

    @abstractmethod
    def get_history(self, client_id: str) -> List[Message]:
        pass

    @abstractmethod
    def add_message(self, client_id: str, sender: MessageSender, content: str) -> None:
        pass

    @abstractmethod
    def client_exists(self, client_id: str) -> bool:
        pass