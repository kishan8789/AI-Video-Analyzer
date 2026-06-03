"""Vector store service for managing embeddings and semantic search."""

import os
from typing import List, Dict, Any, Tuple
import chromadb
from langchain_openai import OpenAIEmbeddings
from config import get_settings


class VectorStoreService:
    """Manages vector database operations using ChromaDB."""

    def __init__(self):
        """Initialize vector store."""
        settings = get_settings()
        self.db_path = settings.vector_db_path
        os.makedirs(self.db_path, exist_ok=True)

        # Initialize ChromaDB with persistent storage (new API)
        self.client = chromadb.PersistentClient(path=self.db_path)

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=settings.embeddings_model,
            openai_api_key=settings.openai_api_key,
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="video_transcripts",
            metadata={"hnsw:space": "cosine"},
        )

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i : i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    def add_video_transcript(
        self,
        video_id: str,
        platform: str,
        transcript: str,
        metadata: Dict[str, Any],
    ) -> int:
        """Add video transcript to vector store."""
        # Handle empty transcripts
        if not transcript or not transcript.strip():
            print(f"Warning: Empty transcript for video {video_id}, skipping vector store")
            return 0
        
        chunks = self.chunk_text(transcript)
        
        # Skip if no valid chunks created
        if not chunks:
            print(f"Warning: No chunks created for video {video_id}")
            return 0
        
        documents = []
        metadatas = []
        ids = []

        for idx, chunk in enumerate(chunks):
            doc_id = f"{video_id}_chunk_{idx}"
            documents.append(chunk)
            metadatas.append(
                {
                    "video_id": video_id,
                    "platform": platform,
                    "chunk_index": idx,
                    "title": metadata.get("title", ""),
                    "creator": metadata.get("creator", ""),
                }
            )
            ids.append(doc_id)

        # Add to collection only if we have documents
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
            )

        return len(chunks)

    def query(
        self,
        query_text: str,
        video_ids: List[str] = None,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Query vector store for similar chunks."""
        where_filter = None
        if video_ids:
            # Build filter for specific video IDs
            where_filter = {"video_id": {"$in": video_ids}}

        results = self.collection.query(
            query_texts=[query_text],
            where=where_filter,
            n_results=top_k,
        )

        # Format results
        formatted_results = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append(
                    {
                        "text": doc,
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if "distances" in results else None,
                    }
                )

        return formatted_results

    def delete_video(self, video_id: str) -> None:
        """Delete all chunks for a video."""
        # Get all documents with this video_id
        results = self.collection.get(
            where={"video_id": {"$eq": video_id}},
        )

        if results and results["ids"]:
            self.collection.delete(ids=results["ids"])

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        count = self.collection.count()
        return {
            "total_chunks": count,
            "collection_name": "video_transcripts",
        }

    def clear_all(self) -> None:
        """Clear entire collection (use with caution)."""
        # Delete and recreate collection
        self.client.delete_collection(name="video_transcripts")
        self.collection = self.client.get_or_create_collection(
            name="video_transcripts",
            metadata={"hnsw:space": "cosine"},
        )
