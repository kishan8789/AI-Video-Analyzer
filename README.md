# 🎥 RAG Video Chatbot

A sophisticated AI-powered application for comparing YouTube and Instagram videos using Retrieval-Augmented Generation (RAG). The chatbot analyzes video transcripts, metadata, and engagement metrics to provide intelligent insights about content performance.

## ✨ Features

- **Multi-Platform Analysis**: Compare YouTube videos and Instagram Reels
- **RAG Pipeline**: Retrieval-Augmented Generation for context-aware responses
- **Vector Database**: ChromaDB for efficient semantic search
- **Streaming Chat**: Real-time streaming responses with Server-Sent Events (SSE)
- **Engagement Metrics**: Automatic calculation of engagement rates and performance comparisons
- **Conversation Memory**: Multi-turn conversations with context awareness
- **Responsive UI**: Modern Next.js frontend with Tailwind CSS styling

## 🏗️ Project Structure

```
chatbot/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── models.py          # Pydantic models
│   │   ├── services/          # Business logic
│   │   │   ├── video_fetcher.py       # Video data fetching
│   │   │   ├── vector_store.py        # ChromaDB management
│   │   │   ├── rag_pipeline.py        # LLM & RAG logic
│   │   │   ├── memory.py              # Conversation memory
│   │   │   └── social_apis.py         # Social platform APIs
│   │   └── utils/             # Helper functions
│   ├── config.py              # Configuration management
│   ├── main.py                # FastAPI app entry point
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile             # Docker configuration
│
├── frontend/                   # Next.js React frontend
│   ├── src/
│   │   ├── app/               # Next.js app router
│   │   ├── components/        # React components
│   │   │   ├── ChatPanel.tsx       # Chat interface
│   │   │   ├── VideoCards.tsx      # Video display
│   │   │   ├── URLInput.tsx        # URL input form
│   │   │   └── ChatPanelImproved.tsx
│   │   └── globals.css        # Global styles
│   ├── package.json           # Node dependencies
│   ├── tailwind.config.ts      # Tailwind CSS config
│   ├── next.config.ts         # Next.js config
│   └── Dockerfile             # Docker configuration
│
├── docker-compose.yml         # Docker Compose orchestration
├── setup.sh                   # Linux/Mac setup script
├── setup.bat                  # Windows setup script
├── deploy.sh                  # Production deployment script
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python** 3.11+
- **Node.js** 18+ and npm
- **OpenAI API Key** (for GPT-4)
- **Docker** & **Docker Compose** (optional, for containerized deployment)

### Local Development Setup

#### 1. Clone and Navigate
```bash
cd chatbot
```

#### 2. Backend Setup

**On macOS/Linux:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OpenAI API key
```

**On Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env and add your OpenAI API key
```

#### 3. Frontend Setup

```bash
cd ../frontend
npm install

# Create .env.local file
cp .env.local.example .env.local
```

#### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
python main.py
# Backend runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:3000
```

Open your browser and navigate to **http://localhost:3000**

### Using Automated Setup Scripts

**On macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```bash
setup.bat
```

## 🐳 Docker Deployment

### Build and Run with Docker Compose

```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Stop services
docker-compose down
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Configuration

### Backend Configuration (.env)

```env
# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# YouTube API (optional)
YOUTUBE_API_KEY=your_youtube_api_key_here

# LLM Configuration
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0.7
EMBEDDINGS_MODEL=text-embedding-3-small

# Vector Database
VECTOR_DB_PATH=./vector_store

# Backend Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
ENVIRONMENT=development
```

### Frontend Configuration (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🔌 API Endpoints

### Video Analysis
- **POST** `/api/videos/analyze` - Analyze YouTube and Instagram videos
  - Request: `{youtube_url: string, instagram_url: string}`
  - Response: Video metadata and engagement metrics

### Chat
- **POST** `/api/chat` - Stream RAG-powered chat responses
  - Request: `{message: string, video_ids: string[], conversation_history: ChatMessage[]}`
  - Response: Server-Sent Events (SSE) stream

### Video Metadata
- **GET** `/api/videos/{video_id}` - Get detailed video information
- **POST** `/api/compare` - Compare videos side by side

### Health Check
- **GET** `/api/health` - Service health status

### Documentation
- **GET** `/docs` - Interactive API documentation (Swagger UI)

## 📊 How It Works

### 1. Video Analysis Phase
- Extracts video ID from provided URLs
- Fetches transcripts using `youtube-transcript-api` and `yt-dlp`
- Retrieves metadata (views, likes, comments, engagement rate)
- Calculates engagement metrics

### 2. Vector Database Phase
- Chunks transcripts into overlapping segments
- Converts chunks to embeddings using OpenAI's `text-embedding-3-small`
- Stores embeddings in ChromaDB with metadata

### 3. RAG Query Phase
- User asks a question via the chat interface
- Query is converted to embeddings
- Similar transcript chunks are retrieved using semantic search
- Retrieved context is passed to GPT-4 with the user's question
- LLM generates contextual response with source citations

### 4. Streaming Response
- Response streams in real-time via SSE
- Frontend displays message chunks as they arrive
- Maintains conversation history for multi-turn interactions

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **LLM**: OpenAI GPT-4
- **Vector DB**: ChromaDB
- **Embeddings**: OpenAI text-embedding-3-small
- **RAG**: LangChain
- **Video Fetching**: yt-dlp, youtube-transcript-api
- **Async**: AsyncIO, HTTPX

### Frontend
- **Framework**: Next.js 14
- **Runtime**: React 18
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Markdown**: react-markdown

### DevOps
- **Containerization**: Docker, Docker Compose
- **Python Version**: 3.11
- **Node Version**: 18 (Alpine)

## 📦 Key Dependencies

### Backend (requirements.txt)
```
fastapi==0.104.1
uvicorn==0.24.0
openai==1.3.9
langchain==0.1.7
chromadb==0.4.17
youtube-transcript-api==0.6.2
yt-dlp==2024.1.31
pydantic==2.5.0
```

### Frontend (package.json)
```json
{
  "next": "^14.0.0",
  "react": "^18.2.0",
  "axios": "^1.6.0",
  "tailwindcss": "^3.3.0"
}
```

## 🔐 Security Considerations

- API keys are loaded from environment variables only
- CORS is configured to accept requests from `localhost:3000` and `localhost:3001`
- In production, update CORS origins in `config.py`
- Input sanitization is applied to user messages
- Use HTTPS in production
- Store `.env` files in `.gitignore` (already configured)

## 🐛 Troubleshooting

### OpenAI API Key Error
- Ensure `OPENAI_API_KEY` is set in `.env`
- Verify API key is valid and has sufficient quota
- Check OpenAI billing and usage limits

### YouTube Transcript Not Available
- Some videos have disabled transcripts
- The app gracefully handles missing transcripts
- Check if video URL is valid and public

### Vector Database Issues
- Delete `./backend/vector_store` directory to reset database
- Ensure write permissions in backend directory

### Port Already in Use
- Backend: Change `BACKEND_PORT` in `.env`
- Frontend: Change port in `npm run dev -- -p <port>`

### Docker Issues
- Run `docker-compose down -v` to remove volumes
- Rebuild with `docker-compose build --no-cache`

## 📈 Performance Tips

- Adjust `chunk_size` and `overlap` in `rag_pipeline.py` for faster retrieval
- Use `EMBEDDINGS_MODEL=text-embedding-3-large` for better accuracy (slower)
- Cache frequently asked questions in conversation memory
- Use `LLM_TEMPERATURE=0.3` for more consistent responses

## 🚀 Production Deployment

### Using Docker Compose
```bash
docker-compose -f docker-compose.yml up -d
```

### Environment Variables
Update for production:
- `ENVIRONMENT=production`
- `BACKEND_HOST=0.0.0.0`
- Update CORS origins to your domain
- Use a production-grade database instead of file-based ChromaDB

### Health Checks
Both services include health check endpoints:
- Backend: `GET /api/health`
- Frontend: `GET /` (HTTP 200)

## 📚 Documentation

- **API Docs**: Visit `http://localhost:8000/docs` for interactive Swagger UI
- **LangChain**: https://docs.langchain.com/
- **ChromaDB**: https://docs.trychroma.com/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Next.js**: https://nextjs.org/docs

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🎓 Learning Resources

This project demonstrates:
- Retrieval-Augmented Generation (RAG) patterns
- Vector database usage with ChromaDB
- FastAPI async/await patterns
- Server-Sent Events (SSE) streaming
- Next.js server components and client-side data fetching
- Docker containerization
- LangChain integration

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at `/docs`
3. Check application logs for error messages

---

**Happy video analyzing! 🎬**
