# Development Guide

This document provides detailed information for developers working on the RAG Video Chatbot project.

## Project Overview

The RAG Video Chatbot is a full-stack application that demonstrates:
- **Retrieval-Augmented Generation (RAG)** using LangChain
- **Vector Database** operations with ChromaDB
- **Async FastAPI** backend for concurrent request handling
- **Next.js** modern frontend with real-time streaming
- **Server-Sent Events (SSE)** for streaming responses
- **Docker** containerization for consistent deployments

## Architecture

### Backend Architecture

```
FastAPI Server
├── API Routes (/api/videos/analyze, /api/chat, etc.)
├── Services Layer
│   ├── VideoFetcher: YouTube/Instagram data extraction
│   ├── VectorStoreService: ChromaDB operations
│   ├── RAGPipeline: LLM query orchestration
│   ├── ConversationMemory: Multi-turn context management
│   └── Social APIs: Placeholder for API integrations
├── Models: Pydantic data validation
├── Utils: Helpers and utilities
└── Config: Environment management
```

### Frontend Architecture

```
Next.js App (React 18)
├── Server Components (layout, root)
├── Client Components (page, components)
│   ├── ChatPanel: Chat interface with streaming
│   ├── URLInput: Video URL input form
│   └── VideoCards: Video metadata display
└── Utilities: HTTP client (Axios)
```

### Data Flow

```
User Input (URLs)
    ↓
VideoFetcher (YouTube API, yt-dlp)
    ↓
VideoMetadata (title, views, likes, transcript)
    ↓
VectorStore (ChromaDB)
    ├── Chunk transcript
    ├── Generate embeddings
    └── Store with metadata
    ↓
Chat Query
    ├── Vector search for relevant chunks
    ├── RAG pipeline
    └── Stream response via SSE
```

## Directory Structure Explained

### Backend (`backend/`)

```
backend/
├── main.py                 # FastAPI app initialization
├── config.py              # Settings from environment variables
├── requirements.txt       # Python package dependencies
├── Dockerfile             # Container image definition
│
├── app/
│   ├── __init__.py
│   ├── models.py          # Pydantic models for data validation
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py      # API endpoints (analyze, chat, etc.)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── video_fetcher.py     # Video data extraction
│   │   ├── vector_store.py      # ChromaDB operations
│   │   ├── rag_pipeline.py      # LLM and RAG logic
│   │   ├── memory.py            # Conversation memory
│   │   └── social_apis.py       # API templates for production
│   │
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py    # Utility functions
│       └── streaming.py  # SSE streaming utilities
└── venv/                  # Virtual environment (created on setup)
```

### Frontend (`frontend/`)

```
frontend/
├── package.json           # Node dependencies
├── tsconfig.json          # TypeScript config
├── next.config.ts         # Next.js config
├── tailwind.config.ts     # Tailwind CSS config
├── postcss.config.js      # PostCSS plugins
├── Dockerfile             # Container image
│
├── src/
│   ├── app/
│   │   ├── layout.tsx     # Root layout wrapper
│   │   ├── page.tsx       # Home page / main UI
│   │   └── globals.css    # Global styles
│   │
│   └── components/
│       ├── ChatPanel.tsx             # Chat interface component
│       ├── ChatPanelImproved.tsx     # Alternative chat component
│       ├── URLInput.tsx              # URL input form
│       └── VideoCards.tsx            # Video metadata display
│
└── node_modules/          # Dependencies (created on setup)
```

## Key Technologies

### Backend Stack
- **FastAPI**: Modern async web framework
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation and settings management
- **LangChain**: LLM and RAG framework
- **OpenAI**: GPT-4 for intelligent responses
- **ChromaDB**: Vector database for embeddings
- **youtube-transcript-api**: YouTube transcript extraction
- **yt-dlp**: Video metadata extraction

### Frontend Stack
- **Next.js 14**: React framework with app router
- **React 18**: UI library
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **react-markdown**: Markdown rendering
- **TypeScript**: Type-safe JavaScript

## Development Workflow

### Setting Up Development Environment

1. **Clone and setup:**
   ```bash
   cd chatbot
   chmod +x setup.sh start.sh validate.sh  # On Unix-like systems
   ./validate.sh                            # Check everything
   ```

2. **Backend setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
   pip install -r requirements.txt
   ```

3. **Frontend setup:**
   ```bash
   cd frontend
   npm install
   ```

### Running Tests

Currently, the project doesn't have automated tests. To manually test:

1. **Backend health check:**
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **API documentation:**
   ```bash
   curl http://localhost:8000/docs
   ```

3. **Frontend accessibility:**
   ```bash
   curl http://localhost:3000
   ```

### Adding New Features

#### Adding a new API endpoint

1. Create a new function in `backend/app/api/routes.py`:
   ```python
   @router.post("/api/new-endpoint")
   async def new_endpoint(request: RequestModel):
       """Endpoint description."""
       # Implementation
       return {"status": "success", "data": result}
   ```

2. Create a corresponding model in `backend/app/models.py`:
   ```python
   class RequestModel(BaseModel):
       field1: str = Field(..., description="Field description")
       field2: int = Field(default=0)
   ```

#### Adding a new React component

1. Create component in `frontend/src/components/NewComponent.tsx`:
   ```tsx
   'use client'
   
   export default function NewComponent() {
       return <div>Component content</div>
   }
   ```

2. Import and use in pages or other components:
   ```tsx
   import NewComponent from '@/components/NewComponent'
   ```

## Common Issues & Solutions

### Issue: OpenAI API key not recognized
- **Solution**: Ensure `.env` has `OPENAI_API_KEY=your_actual_key`
- Verify API key is valid: https://platform.openai.com/api-keys
- Check rate limits and billing status

### Issue: YouTube transcript not available
- **Solution**: Some videos have disabled transcripts. This is graceful - the app continues.
- Check if video URL is correct and video is public
- Try with a different video

### Issue: Port already in use
- **Backend**: Change `BACKEND_PORT` in `.env`
- **Frontend**: `npm run dev -- -p 3001`

### Issue: Virtual environment not activating
- **Linux/Mac**: Use full path: `source ./venv/bin/activate`
- **Windows**: `venv\Scripts\activate.bat` (not .sh)
- Ensure you're in the correct directory

### Issue: Module not found errors
- Backend: Re-run `pip install -r requirements.txt` in activated venv
- Frontend: Re-run `npm install` and clear cache: `npm cache clean --force`

## Performance Optimization

### Backend Optimization
1. **Increase chunk size** for faster embedding (trade-off: less precision)
   ```python
   # In rag_pipeline.py
   chunks = self.chunk_text(transcript, chunk_size=1000)
   ```

2. **Use batch queries** for multiple videos
3. **Cache embeddings** for repeated queries
4. **Use smaller embedding model** if needed (trade-off: less accurate)

### Frontend Optimization
1. **Memoize components** with `React.memo()`
2. **Use lazy loading** for heavy components
3. **Optimize images** before serving
4. **Enable compression** in Next.js config

## Debugging

### Backend Debugging
1. **Enable debug logs:**
   ```python
   # In main.py
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Use FastAPI debug mode:**
   ```python
   # In main.py
   uvicorn.run(..., debug=True)
   ```

3. **Check ChromaDB logs:**
   ```python
   # In vector_store.py
   print(f"Documents added: {self.collection.count()}")
   ```

### Frontend Debugging
1. **Enable React DevTools:**
   - Install React DevTools browser extension
   - Check component re-renders

2. **Network inspection:**
   - Open browser DevTools
   - Check Network tab for API calls
   - Check Console for errors

3. **Streaming debug:**
   ```typescript
   // In ChatPanel.tsx
   console.log('Raw response:', response)
   console.log('Chunk:', chunk)
   ```

## Git Workflow

### Branch naming
- Feature: `feature/descriptive-name`
- Bug fix: `bugfix/descriptive-name`
- Documentation: `docs/descriptive-name`

### Commit messages
```
feat: Add new feature
fix: Fix bug description
docs: Update documentation
refactor: Refactor code
test: Add tests
```

### Before committing
1. Run validation: `./validate.sh`
2. Check `.gitignore` to avoid committing sensitive data
3. Ensure no secrets in code

## Deployment

### Docker Deployment
```bash
docker-compose build
docker-compose up -d
```

### Production Considerations
1. Update `ENVIRONMENT=production` in `.env`
2. Use production database (PostgreSQL, MongoDB)
3. Add HTTPS/SSL
4. Set up proper CORS origins
5. Implement rate limiting
6. Add monitoring and logging
7. Use environment-specific configs

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://docs.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [OpenAI API Reference](https://platform.openai.com/docs)

## Contributing

1. Create a feature branch
2. Make changes and test locally
3. Update documentation if needed
4. Submit pull request with description
5. Wait for review and feedback

## License

This project is open source under MIT License.
