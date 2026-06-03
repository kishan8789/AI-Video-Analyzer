"""API utilities for response formatting and error handling."""

from fastapi.responses import StreamingResponse
from typing import AsyncGenerator, Any
import json


class StreamingSSE:
    """Helper for Server-Sent Events streaming."""

    @staticmethod
    async def stream_json(
        generator: AsyncGenerator[str, None],
    ) -> AsyncGenerator[bytes, None]:
        """Convert string chunks to SSE format."""
        try:
            async for chunk in generator:
                if chunk:
                    # Escape newlines in JSON
                    data = json.dumps({"content": chunk})
                    yield f"data: {data}\n\n".encode('utf-8')
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n".encode('utf-8')

    @staticmethod
    def create_response(
        generator: AsyncGenerator[str, None],
        media_type: str = "text/event-stream",
    ) -> StreamingResponse:
        """Create streaming response."""
        return StreamingResponse(
            StreamingSSE.stream_json(generator),
            media_type=media_type,
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
