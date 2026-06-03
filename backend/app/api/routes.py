"""API routes for video analysis and RAG chat."""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any
import asyncio
import json

from app.models import (
    AnalysisRequest,
    ChatRequest,
    ChatResponse,
    VideoMetadata,
)
from app.services.video_fetcher import VideoFetcher
from app.services.vector_store import VectorStoreService
from app.services.rag_pipeline import RAGPipeline

router = APIRouter(prefix="/api", tags=["api"])

# Global instances
vector_store = VectorStoreService()
rag_pipeline = RAGPipeline()
video_fetcher = VideoFetcher()

# In-memory storage for videos (in production, use database)
stored_videos: Dict[str, VideoMetadata] = {}


@router.post("/videos/analyze")
async def analyze_videos(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Analyze YouTube and Instagram videos.
    Fetches transcripts, metadata, computes engagement rates, and stores in vector DB.
    """
    try:
        # Fetch video A (YouTube)
        video_a = video_fetcher._fetch_youtube(request.youtube_url, "A")
        stored_videos["A"] = video_a

        # Store in vector DB
        vector_store.add_video_transcript(
            video_id="A",
            platform="youtube",
            transcript=video_a.transcript,
            metadata={
                "title": video_a.title,
                "creator": video_a.creator,
                "views": video_a.views,
                "likes": video_a.likes,
            },
        )

        # Fetch video B (Instagram) - with timeout handling since Instagram fetching is limited
        try:
            video_b = video_fetcher._fetch_instagram(request.instagram_url, "B")
            stored_videos["B"] = video_b

            vector_store.add_video_transcript(
                video_id="B",
                platform="instagram",
                transcript=video_b.transcript,
                metadata={
                    "title": video_b.title,
                    "creator": video_b.creator,
                    "views": video_b.views,
                    "likes": video_b.likes,
                },
            )
        except Exception as e:
            # Instagram fetching might fail due to anti-scraping measures
            # Still return success with video A data
            print(f"Warning: Could not fetch Instagram video fully: {e}")
            # Create a placeholder for video B
            video_b = VideoMetadata(
                video_id="B",
                platform="instagram",
                url=request.instagram_url,
                title="Instagram Reel",
                creator="Unknown Creator",
                follower_count=0,
                views=0,
                likes=0,
                comments=0,
                engagement_rate=0.0,
                duration_seconds=0,
                upload_date="",
                transcript="[Transcript could not be extracted from Instagram video]",
                hashtags=[],
            )
            stored_videos["B"] = video_b

        return {
            "status": "success",
            "videos": {
                "A": {
                    "title": video_a.title,
                    "platform": video_a.platform,
                    "creator": video_a.creator,
                    "engagement_rate": round(video_a.engagement_rate, 2),
                    "views": video_a.views,
                    "likes": video_a.likes,
                },
                "B": {
                    "title": video_b.title,
                    "platform": video_b.platform,
                    "creator": video_b.creator,
                    "engagement_rate": round(video_b.engagement_rate, 2),
                    "views": video_b.views,
                    "likes": video_b.likes,
                },
            },
            "message": "Videos analyzed and stored successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing videos: {str(e)}")


@router.post("/chat")
async def chat_streaming(request: ChatRequest):
    """
    Stream chat responses with RAG.
    Supports multi-turn conversations with memory.
    """

    async def generate():
        """Generator for streaming response."""
        try:
            # Build conversation history
            conversation_history = []
            if request.conversation_history:
                for msg in request.conversation_history:
                    # Handle both ChatMessage objects and dicts
                    if isinstance(msg, dict):
                        conversation_history.append(msg)
                    else:
                        conversation_history.append(
                            {
                                "role": msg.role,
                                "content": msg.content,
                            }
                        )

            # Get streaming response from RAG
            async for chunk in rag_pipeline.query(
                user_message=request.message,
                video_ids=request.video_ids,
                conversation_history=conversation_history,
            ):
                # Stream as SSE (Server-Sent Events) format
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

            # Send completion signal
            yield "data: {\"done\": true}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.get("/videos/{video_id}")
async def get_video_metadata(video_id: str):
    """Get stored video metadata."""
    if video_id not in stored_videos:
        raise HTTPException(status_code=404, detail=f"Video {video_id} not found")

    video = stored_videos[video_id]
    return {
        "video_id": video.video_id,
        "platform": video.platform,
        "title": video.title,
        "creator": video.creator,
        "follower_count": video.follower_count,
        "views": video.views,
        "likes": video.likes,
        "comments": video.comments,
        "engagement_rate": round(video.engagement_rate, 2),
        "duration_seconds": video.duration_seconds,
        "upload_date": video.upload_date,
        "hashtags": video.hashtags,
        "thumbnail_url": video.thumbnail_url,
    }


@router.post("/compare")
async def compare_videos(video_ids: list[str] = ["A", "B"]):
    """Compare two videos side by side."""
    videos_data = {}

    for vid in video_ids:
        if vid not in stored_videos:
            raise HTTPException(status_code=404, detail=f"Video {vid} not found")

        video = stored_videos[vid]
        videos_data[vid] = {
            "title": video.title,
            "creator": video.creator,
            "views": video.views,
            "likes": video.likes,
            "comments": video.comments,
            "engagement_rate": round(video.engagement_rate, 2),
            "likes_per_1k_views": round((video.likes / video.views * 1000), 2)
            if video.views > 0
            else 0,
            "comments_per_1k_views": round((video.comments / video.views * 1000), 2)
            if video.views > 0
            else 0,
        }

    return {
        "comparison": videos_data,
        "message": "Comparison generated successfully",
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "RAG Chatbot Backend",
        "vector_store_stats": vector_store.get_collection_stats(),
    }
