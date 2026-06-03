"""Service for fetching video data from various platforms."""

import re
import json
from typing import Dict, Any, Optional
from datetime import datetime

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from app.models import VideoMetadata


class VideoFetcher:
    """Fetches video data including transcripts and metadata."""

    @staticmethod
    def extract_youtube_id(url: str) -> str:
        """Extract video ID from YouTube URL."""
        patterns = [
            r"youtube\.com/watch\?v=([^&\n?#]+)",
            r"youtu\.be/([^&\n?#]+)",
            r"youtube\.com/embed/([^&\n?#]+)",
            r"youtube\.com/shorts/([^&\n?#]+)",  # YouTube Shorts
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError(f"Invalid YouTube URL: {url}")

    @staticmethod
    def extract_instagram_id(url: str) -> str:
        """Extract Reel ID from Instagram URL."""
        patterns = [
            r"instagram\.com/reels/([^/?&\n]+)",
            r"instagram\.com/p/([^/?&\n]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError(f"Invalid Instagram URL: {url}")

    @staticmethod
    def fetch_youtube_transcript(video_id: str) -> str:
        """Fetch transcript from YouTube."""
        try:
            transcripts = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([item["text"] for item in transcripts])
        except Exception as e:
            print(f"Error fetching YouTube transcript: {e}")
            # Fallback: Return a message indicating transcript unavailable
            # This prevents empty string from breaking the vector store
            return f"[Transcript unavailable for video {video_id}. This could be due to: no captions available, video is private, or transcript is restricted. Please ensure the video has captions enabled.]"

    @staticmethod
    def fetch_youtube_metadata(url: str, video_id: str) -> Dict[str, Any]:
        """Fetch YouTube video metadata using yt-dlp."""
        try:
            with yt_dlp.YoutubeDL(
                {
                    "quiet": True,
                    "no_warnings": True,
                    "extract_flat": False,
                }
            ) as ydl:
                info = ydl.extract_info(url, download=False)

            return {
                "title": info.get("title", ""),
                "creator": info.get("uploader", ""),
                "follower_count": info.get("channel_follower_count", 0) or 0,
                "views": info.get("view_count", 0) or 0,
                "likes": info.get("like_count", 0) or 0,
                "comments": info.get("comment_count", 0) or 0,
                "duration_seconds": info.get("duration", 0) or 0,
                "upload_date": info.get("upload_date", ""),
                "thumbnail_url": info.get("thumbnail", ""),
                "hashtags": info.get("tags", []) or [],
            }
        except Exception as e:
            print(f"Error fetching YouTube metadata: {e}")
            return {}

    @staticmethod
    def fetch_instagram_metadata(url: str) -> Dict[str, Any]:
        """
        Fetch Instagram Reel metadata.
        Note: Instagram has anti-scraping measures. This is a basic implementation.
        For production, consider using Instagram Graph API or a service like Apify.
        """
        # Note: Direct scraping Instagram is difficult due to their restrictions
        # This is a placeholder - in production, use Instagram Graph API
        print(
            "Note: Instagram fetching requires Graph API credentials or external service"
        )

        return {
            "title": "Instagram Reel",
            "creator": "Unknown",
            "follower_count": 0,
            "views": 0,
            "likes": 0,
            "comments": 0,
            "duration_seconds": 0,
            "upload_date": "",
            "thumbnail_url": None,
            "hashtags": [],
        }

    @staticmethod
    def fetch_instagram_transcript(url: str) -> str:
        """
        Fetch Instagram Reel transcript using Whisper.
        Downloads video and extracts audio, then transcribes.
        """
        try:
            with yt_dlp.YoutubeDL(
                {
                    "quiet": True,
                    "no_warnings": True,
                    "extract_audio": True,
                    "audio_format": "mp3",
                    "audio_quality": "192",
                }
            ) as ydl:
                info = ydl.extract_info(url, download=True)
                audio_file = ydl.prepare_filename(info)

            # TODO: Use Whisper to transcribe audio_file
            # from openai import OpenAI
            # client = OpenAI()
            # with open(audio_file, "rb") as f:
            #     transcript = client.audio.transcriptions.create(
            #         model="whisper-1", file=f
            #     )
            # return transcript.text

            return "[Instagram Reel content analysis requires Whisper transcription implementation]"
        except Exception as e:
            print(f"Error fetching Instagram transcript: {e}")
            return f"[Instagram Reel transcript unavailable: {str(e)}. Instagram has anti-scraping measures. For production use, integrate with Instagram Graph API.]"

    @staticmethod
    def compute_engagement_rate(likes: int, comments: int, views: int) -> float:
        """Compute engagement rate as percentage."""
        if views == 0:
            return 0.0
        return ((likes + comments) / views) * 100

    @staticmethod
    async def fetch_video(url: str, video_id: str) -> VideoMetadata:
        """Fetch complete video data (metadata + transcript)."""

        if "youtube.com" in url or "youtu.be" in url:
            return VideoFetcher._fetch_youtube(url, video_id)
        elif "instagram.com" in url:
            return VideoFetcher._fetch_instagram(url, video_id)
        else:
            raise ValueError(f"Unsupported platform in URL: {url}")

    @staticmethod
    def _fetch_youtube(url: str, video_id: str) -> VideoMetadata:
        """Fetch YouTube video."""
        youtube_id = VideoFetcher.extract_youtube_id(url)
        metadata = VideoFetcher.fetch_youtube_metadata(url, youtube_id)
        transcript = VideoFetcher.fetch_youtube_transcript(youtube_id)

        engagement_rate = VideoFetcher.compute_engagement_rate(
            metadata.get("likes", 0), metadata.get("comments", 0), metadata.get("views", 0)
        )

        return VideoMetadata(
            video_id=video_id,
            platform="youtube",
            url=url,
            title=metadata.get("title", ""),
            creator=metadata.get("creator", ""),
            follower_count=metadata.get("follower_count", 0),
            views=metadata.get("views", 0),
            likes=metadata.get("likes", 0),
            comments=metadata.get("comments", 0),
            engagement_rate=engagement_rate,
            duration_seconds=metadata.get("duration_seconds", 0),
            upload_date=metadata.get("upload_date", ""),
            transcript=transcript,
            hashtags=metadata.get("hashtags", []),
            thumbnail_url=metadata.get("thumbnail_url"),
        )

    @staticmethod
    def _fetch_instagram(url: str, video_id: str) -> VideoMetadata:
        """Fetch Instagram Reel."""
        instagram_id = VideoFetcher.extract_instagram_id(url)
        metadata = VideoFetcher.fetch_instagram_metadata(url)
        transcript = VideoFetcher.fetch_instagram_transcript(url)

        engagement_rate = VideoFetcher.compute_engagement_rate(
            metadata.get("likes", 0), metadata.get("comments", 0), metadata.get("views", 0)
        )

        return VideoMetadata(
            video_id=video_id,
            platform="instagram",
            url=url,
            title=metadata.get("title", ""),
            creator=metadata.get("creator", ""),
            follower_count=metadata.get("follower_count", 0),
            views=metadata.get("views", 0),
            likes=metadata.get("likes", 0),
            comments=metadata.get("comments", 0),
            engagement_rate=engagement_rate,
            duration_seconds=metadata.get("duration_seconds", 0),
            upload_date=metadata.get("upload_date", ""),
            transcript=transcript,
            hashtags=metadata.get("hashtags", []),
            thumbnail_url=metadata.get("thumbnail_url"),
        )
