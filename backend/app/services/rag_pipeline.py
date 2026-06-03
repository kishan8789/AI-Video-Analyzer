"""RAG pipeline using LangChain for intelligent Q&A."""

from typing import List, Dict, Any, AsyncGenerator
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config import get_settings
from app.services.vector_store import VectorStoreService


class RAGPipeline:
    """Orchestrates retrieval-augmented generation for video analysis."""

    def __init__(self):
        """Initialize RAG pipeline."""
        settings = get_settings()
        self.vector_store = VectorStoreService()
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            openai_api_key=settings.openai_api_key,
            streaming=True,
        )

        self.system_prompt = """You are an expert video analyst helping content creators optimize their content based on engagement metrics and performance comparisons.

You have access to transcripts and metadata from multiple videos. Use this information to:
1. Compare engagement metrics and performance
2. Analyze what hooks work in the first 5 seconds
3. Provide actionable insights for improvement
4. Reference specific creators and their follower counts
5. Suggest optimizations based on what worked in high-performing videos

Always cite your sources by mentioning which video (A or B) and what transcript segment you're referencing.
Be specific, data-driven, and actionable in your recommendations."""

    async def query(
        self,
        user_message: str,
        video_ids: List[str],
        conversation_history: List[Dict[str, str]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Execute RAG query with streaming response.

        Yields: Streaming response chunks as strings.
        """
        if conversation_history is None:
            conversation_history = []

        # Retrieve relevant context from vector store
        context_results = self.vector_store.query(
            query_text=user_message,
            video_ids=video_ids,
            top_k=5,
        )

        # Format context
        context_text = self._format_context(context_results)

        # Build messages for LLM
        messages = self._build_messages(
            user_message=user_message,
            context=context_text,
            conversation_history=conversation_history,
        )

        # Stream response
        async for chunk in self._stream_response(messages):
            yield chunk

    def _format_context(self, results: List[Dict[str, Any]]) -> str:
        """Format retrieved context for LLM."""
        context_parts = []
        for i, result in enumerate(results, 1):
            metadata = result.get("metadata", {})
            text = result.get("text", "")
            video_id = metadata.get("video_id", "Unknown")
            platform = metadata.get("platform", "unknown")

            context_parts.append(
                f"\n[Source: Video {video_id} ({platform}), Chunk {metadata.get('chunk_index', 0)}]\n{text}"
            )

        return "".join(context_parts) if context_parts else "[No relevant context found]"

    def _build_messages(
        self,
        user_message: str,
        context: str,
        conversation_history: List[Dict[str, str]],
    ) -> List[Any]:
        """Build message list for LLM."""
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]

        # Add conversation history
        for msg in conversation_history:
            if msg["role"] == "user":
                messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                messages.append({"role": "assistant", "content": msg["content"]})

        # Add context and current user message
        messages.append(
            {
                "role": "user",
                "content": f"""Context from video transcripts:
{context}

User Question:
{user_message}

Please provide a detailed, specific answer with source citations.""",
            }
        )

        return messages

    async def _stream_response(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        """Stream response from LLM."""
        try:
            # Convert to LangChain message format
            lc_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    lc_messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    lc_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    lc_messages.append(AIMessage(content=msg["content"]))

            # Stream response
            response = self.llm.stream(lc_messages)
            for chunk in response:
                if chunk.content:
                    yield chunk.content

        except Exception as e:
            yield f"Error processing query: {str(e)}"

    def extract_sources_from_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Extract source citations from response text."""
        sources = []
        # Look for patterns like "Video A" or "Video B"
        import re

        video_mentions = re.findall(r"Video ([AB])", response_text)
        for video_id in set(video_mentions):
            sources.append(
                {
                    "video_id": video_id,
                    "mentioned_in_response": True,
                }
            )

        return sources
