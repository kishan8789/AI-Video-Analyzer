"""
Advanced RAG Pipeline with Conversation Memory and Better Streaming

This module provides an improved RAG pipeline with better context management.
"""

from typing import List, Dict, Any, AsyncGenerator, Optional
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from config import get_settings
from app.services.vector_store import VectorStoreService
from app.services.memory import ConversationMemory


class AdvancedRAGPipeline:
    """Advanced RAG pipeline with memory management and better streaming."""

    def __init__(self):
        """Initialize advanced RAG pipeline."""
        settings = get_settings()
        self.vector_store = VectorStoreService()
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            openai_api_key=settings.openai_api_key,
            streaming=True,
            max_tokens=1000,
        )
        self.conversation_memory = ConversationMemory(max_history=15)

    def _build_system_prompt(self) -> str:
        """Build context-aware system prompt."""
        return """You are an expert video analyst and content strategist helping creators optimize their videos for engagement.

Your expertise includes:
- Analyzing engagement metrics and trends
- Comparing content performance
- Identifying what makes content go viral
- Providing actionable recommendations

When answering questions:
1. ALWAYS reference specific videos (Video A or Video B) and their metrics
2. Cite transcript excerpts when discussing content specifics
3. Provide data-driven analysis with percentages and comparisons
4. Suggest concrete, implementable improvements
5. Be specific about timestamps when discussing video sections

Format your responses with:
- Direct answer to the question
- Supporting evidence from the videos
- Specific metrics (engagement rates, view counts, etc.)
- Actionable recommendations"""

    async def query(
        self,
        user_message: str,
        video_ids: List[str],
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Execute RAG query with streaming and memory.

        Yields: Streaming response chunks as strings.
        """
        if conversation_history is None:
            conversation_history = []

        # Add to memory
        self.conversation_memory.add_message("user", user_message)

        # Retrieve context from vector store
        context_results = self.vector_store.query(
            query_text=user_message,
            video_ids=video_ids,
            top_k=6,  # Increased for better context
        )

        # Format context with metadata
        context_text = self._format_context_with_metadata(context_results)

        # Build messages
        messages = self._build_messages_with_memory(
            user_message=user_message,
            context=context_text,
            conversation_history=conversation_history,
        )

        # Stream response
        full_response = ""
        async for chunk in self._stream_response(messages):
            full_response += chunk
            yield chunk

        # Add response to memory
        self.conversation_memory.add_message("assistant", full_response)

    def _format_context_with_metadata(self, results: List[Dict[str, Any]]) -> str:
        """Format retrieved context with rich metadata."""
        if not results:
            return "[No relevant context found in videos]"

        context_parts = []
        context_parts.append("=== VIDEO CONTEXT ===\n")

        seen_videos = set()
        for i, result in enumerate(results, 1):
            metadata = result.get("metadata", {})
            text = result.get("text", "")
            video_id = metadata.get("video_id", "Unknown")
            platform = metadata.get("platform", "unknown")
            creator = metadata.get("creator", "Unknown")
            chunk_idx = metadata.get("chunk_index", 0)

            # Add video intro once
            if video_id not in seen_videos:
                context_parts.append(f"\n### Video {video_id} ({platform.upper()})")
                context_parts.append(f"Creator: {creator}\n")
                seen_videos.add(video_id)

            context_parts.append(f"[Chunk {chunk_idx}]\n{text}\n")

        context_parts.append("\n=== END CONTEXT ===\n")
        return "".join(context_parts)

    def _build_messages_with_memory(
        self,
        user_message: str,
        context: str,
        conversation_history: List[Dict[str, str]],
    ) -> List[Any]:
        """Build message list with context and memory."""
        messages = [SystemMessage(content=self._build_system_prompt())]

        # Add conversation history
        for msg in conversation_history[-6:]:  # Last 6 messages
            if msg.get("role") == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg.get("role") == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        # Add current context and query
        user_context = f"""
Video Data Available:
{context}

Question: {user_message}

Please provide a detailed answer with specific metrics and references to the videos."""

        messages.append(HumanMessage(content=user_context))
        return messages

    async def _stream_response(
        self,
        messages: List[Any],
    ) -> AsyncGenerator[str, None]:
        """Stream response from LLM."""
        try:
            response_generator = self.llm.stream(messages)
            for chunk in response_generator:
                if chunk.content:
                    yield chunk.content
        except Exception as e:
            yield f"\n[Error: {str(e)}]"

    def get_memory_summary(self) -> str:
        """Get conversation memory summary."""
        return self.conversation_memory.summarize()

    def clear_memory(self) -> None:
        """Clear conversation memory."""
        self.conversation_memory.clear()
