"""Conversation memory management for multi-turn interactions."""

from typing import List, Dict, Any
from datetime import datetime
from app.models import ChatMessage


class ConversationMemory:
    """Manages conversation history and context."""

    def __init__(self, max_history: int = 10):
        """Initialize conversation memory.

        Args:
            max_history: Maximum number of messages to keep in memory
        """
        self.max_history = max_history
        self.messages: List[ChatMessage] = []
        self.created_at = datetime.utcnow()

    def add_message(self, role: str, content: str, sources: List[str] = None) -> ChatMessage:
        """Add message to conversation memory."""
        message = ChatMessage(
            role=role,
            content=content,
            video_sources=sources,
        )
        self.messages.append(message)

        # Keep only last N messages to avoid context overflow
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history :]

        return message

    def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history as dict list."""
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in self.messages
        ]

    def get_context(self, last_n: int = 5) -> str:
        """Get formatted context for LLM."""
        recent = self.messages[-last_n:]
        context_parts = []

        for msg in recent:
            role = "User" if msg.role == "user" else "Assistant"
            context_parts.append(f"{role}: {msg.content}")

        return "\n".join(context_parts)

    def clear(self) -> None:
        """Clear conversation history."""
        self.messages = []

    def summarize(self) -> str:
        """Summarize conversation (useful for very long conversations)."""
        if not self.messages:
            return "No conversation history"

        first_message = self.messages[0].content[:100]
        last_message = self.messages[-1].content[:100]
        message_count = len(self.messages)

        return f"Conversation with {message_count} messages. Started with: '{first_message}...'. Latest: '{last_message}...'"
