# Quick Reference Guide

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.11+ 
- Node.js 18+
- OpenAI API key

### Installation
```bash
# Linux/Mac
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

### Running
```bash
# Terminal 1 - Backend
./start.sh backend    # or start.bat backend on Windows

# Terminal 2 - Frontend  
./start.sh frontend   # or start.bat frontend on Windows
```

Then open: **http://localhost:3000**

---

## 📁 Project Structure

```
chatbot/
├── backend/          # Python FastAPI backend
├── frontend/         # Next.js React frontend
├── README.md         # Full documentation
├── DEVELOPMENT.md    # Developer guide
├── setup.sh/bat      # Initial setup scripts
├── start.sh/bat      # Start servers
└── validate.sh/bat   # Project validation
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/videos/analyze` | Analyze videos |
| POST | `/api/chat` | Chat with RAG (streaming) |
| GET | `/api/videos/{id}` | Get video metadata |
| POST | `/api/compare` | Compare videos |
| GET | `/api/health` | Health check |
| GET | `/docs` | API documentation |

---

## ⚙️ Configuration

### Backend (.env)
```env
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o
BACKEND_PORT=8000
ENVIRONMENT=development
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🛠️ Common Commands

### Backend
```bash
# Activate environment
source backend/venv/bin/activate  # Linux/Mac
backend\venv\Scripts\activate.bat  # Windows

# Run server
python backend/main.py

# Install packages
pip install -r requirements.txt

# Check health
curl http://localhost:8000/api/health
```

### Frontend
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Start production build
npm start
```

### Docker
```bash
# Build
docker-compose build

# Run
docker-compose up

# Stop
docker-compose down

# Logs
docker-compose logs -f
```

### Validation
```bash
./validate.sh     # Linux/Mac
validate.bat      # Windows
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| OpenAI key error | Check `.env` file and API key validity |
| Port in use | Change port in `.env` or kill process |
| Module not found | Run `pip install -r requirements.txt` |
| Node error | Run `npm install` and clear cache |
| YouTube error | Use valid public video URL |
| Venv not activating | Use full path to activate script |

---

## 📚 Documentation Files

- **README.md** - Full project documentation, features, setup
- **DEVELOPMENT.md** - Developer guide, architecture, contributing
- **API Docs** - Interactive: http://localhost:8000/docs

---

## 🔑 Key Features

✅ Multi-platform video analysis (YouTube, Instagram)  
✅ RAG-powered intelligent chat  
✅ Real-time streaming responses  
✅ Conversation memory  
✅ Engagement metrics comparison  
✅ Docker containerization  
✅ Type-safe code (Python Pydantic, TypeScript)  

---

## 🤝 Common Tasks

### Adding a new API endpoint
1. Add route in `backend/app/api/routes.py`
2. Add model in `backend/app/models.py`
3. Test with `/docs`

### Adding a new React component
1. Create in `frontend/src/components/`
2. Import and use in pages
3. Style with Tailwind CSS

### Updating dependencies
```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm update
```

### Database reset
```bash
# Delete ChromaDB
rm -rf backend/vector_store

# Restart backend
python backend/main.py
```

---

## 📊 Technology Stack

**Backend**: FastAPI, OpenAI, LangChain, ChromaDB, Uvicorn  
**Frontend**: Next.js, React, TypeScript, Tailwind CSS  
**DevOps**: Docker, Docker Compose  

---

## 🔗 Useful Links

- FastAPI: https://fastapi.tiangolo.com/
- LangChain: https://docs.langchain.com/
- ChromaDB: https://docs.trychroma.com/
- Next.js: https://nextjs.org/
- OpenAI: https://platform.openai.com/

---

## 📞 Getting Help

1. Check README.md for full documentation
2. Review DEVELOPMENT.md for architecture details
3. Visit API docs at `http://localhost:8000/docs`
4. Check error logs in terminal output
5. Run validation: `./validate.sh`

---

## ✨ Pro Tips

- Use `npm run dev -- -p <port>` to change frontend port
- Access backend Swagger UI at `http://localhost:8000/docs`
- Check vector store stats at `http://localhost:8000/api/health`
- Use `docker-compose logs -f <service>` to debug
- Set `LLM_TEMPERATURE=0.3` for consistent responses
- Use Chrome DevTools for frontend debugging

---

**Last Updated**: 2024  
**Version**: 1.0.0
