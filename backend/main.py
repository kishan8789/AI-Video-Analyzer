"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import uvicorn

from config import get_settings
from app.api.routes import router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    print("🚀 RAG Chatbot Backend Starting...")
    print(f"Environment: {settings.environment}")
    print(f"LLM Model: {settings.llm_model}")
    print(f"Vector DB Path: {settings.vector_db_path}")
    yield
    # Shutdown
    print("🛑 RAG Chatbot Backend Shutting Down...")


# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Backend API for video comparison and analysis using RAG",
    version="1.0.0",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "RAG Chatbot API is running",
        "docs": "/docs",
        "health": "/api/health",
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.environment == "development",
    )
