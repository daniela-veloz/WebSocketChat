"""Message model for chat application."""
from dataclasses import dataclass
from enum import Enum


class MessageSender(str, Enum):
    SYSTEM = "system"
    USER = "user"


@dataclass
class Message:
    sender: MessageSender
    content: str

    def to_dict(self) -> dict:
        return {
            "sender": self.sender.value,
            "content": self.content
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        sender_str = data.get("sender")
        content = data.get("content")

        if not sender_str:
            raise ValueError("Missing 'sender' field")
        if not content:
            raise ValueError("Missing 'content' field")

        sender = MessageSender(sender_str)

        return cls(sender=sender, content=content)