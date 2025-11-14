import sqlite3
from typing import List

from persistance.ClientDataDb import ClientDataDb
from models.message import Message, MessageSender


class ClientDataSqliteDb(ClientDataDb):
    """SQLite implementation of ClientDataDb."""

    def __init__(self, db_path: str = "webchat.db"):
        """
        Initialize the SQLite database.

        Args:
            db_path: Path to the SQLite database file. Defaults to "chatbot.db"
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self) -> None:
        """Create the necessary tables if they don't exist."""
        cursor = self.conn.cursor()

        # Create clients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id TEXT PRIMARY KEY
            )
        """)

        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(client_id)
            )
        """)

        self.conn.commit()

    def add_client(self, client_id: str) -> None:
        self.validate_client_id(client_id)
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO clients (client_id) VALUES (?)", (client_id,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            # Client already exists, which is fine
            pass

    def add_message(self, client_id: str, sender: MessageSender, content: str) -> None:
        self.validate_client_id(client_id)

        if not self.client_exists(client_id):
            raise ValueError(f"Client {client_id} does not exist. Call add_client first.")

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO messages (client_id, sender, content) VALUES (?, ?, ?)",
            (client_id, sender.value, content)
        )
        self.conn.commit()

    def get_history(self, client_id: str) -> List[Message]:
        self.validate_client_id(client_id)

        if not self.client_exists(client_id):
            raise ValueError(f"Client {client_id} does not exist")

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT sender, content FROM messages WHERE client_id = ? ORDER BY id ASC",
            (client_id,)
        )

        rows = cursor.fetchall()
        messages = []
        for sender_str, content in rows:
            sender = MessageSender(sender_str)
            messages.append(Message(sender=sender, content=content))

        return messages

    def client_exists(self, client_id: str) -> bool:
        self.validate_client_id(client_id)
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM clients WHERE client_id = ?", (client_id,))
        return cursor.fetchone() is not None

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Ensure the connection is closed when the object is destroyed."""
        self.close()