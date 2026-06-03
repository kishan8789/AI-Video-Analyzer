"""Data models for the RAG chatbot."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class VideoMetadata(BaseModel):
    """Video metadata model."""

    video_id: str = Field(..., description="Unique video identifier (A or B)")
    platform: str = Field(..., description="Platform (youtube or instagram)")
    url: str = Field(..., description="Video URL")
    title: str = Field(..., description="Video title")
    creator: str = Field(..., description="Creator/channel name")
    follower_count: int = Field(..., description="Creator follower count")
    views: int = Field(..., description="Total views")
    likes: int = Field(..., description="Total likes")
    comments: int = Field(..., description="Total comments")
    engagement_rate: float = Field(..., description="Engagement rate percentage")
    duration_seconds: int = Field(..., description="Video duration in seconds")
    upload_date: str = Field(..., description="Upload date ISO format")
    transcript: str = Field(..., description="Full video transcript")
    hashtags: List[str] = Field(default_factory=list, description="Video hashtags")
    thumbnail_url: Optional[str] = Field(default=None, description="Thumbnail URL")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AnalysisRequest(BaseModel):
    """Request model for video analysis."""

    youtube_url: str = Field(..., description="YouTube video URL")
    instagram_url: str = Field(..., description="Instagram Reels URL")


class ChatMessage(BaseModel):
    """Chat message model."""

    role: str = Field(..., description="Message role (user or assistant)")
    content: str = Field(..., description="Message content")
    video_sources: Optional[List[str]] = Field(
        default=None, description="Source citations"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Chat request model."""

    message: str = Field(..., description="User message")
    video_ids: List[str] = Field(..., description="Video IDs to query (e.g., ['A', 'B'])")
    conversation_history: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Previous messages for context"
    )


class ChatResponse(BaseModel):
    """Chat response model."""

    message: str = Field(..., description="Assistant response")
    sources: List[Dict[str, Any]] = Field(
        ..., description="Source citations with video_id and chunk info"
    )
    tokens_used: Optional[int] = Field(None, description="Tokens consumed")


class ComparisonRequest(BaseModel):
    """Request for video comparison."""

    metric: str = Field(
        ..., description="Metric to compare (engagement_rate, hooks, creator_info, etc)"
    )
    video_ids: List[str] = Field(..., description="Video IDs to compare")


class ChunkMetadata(BaseModel):
    """Metadata for vector store chunks."""

    video_id: str = Field(..., description="Source video ID")
    platform: str = Field(..., description="Source platform")
    chunk_index: int = Field(..., description="Chunk sequence number")
    timestamp_start: Optional[float] = Field(None, description="Timestamp in seconds")
    timestamp_end: Optional[float] = Field(None, description="Timestamp in seconds")
