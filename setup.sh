#!/bin/bash

# Setup script for RAG Chatbot

echo "🚀 Setting up RAG Chatbot..."

# Backend setup
echo "📦 Setting up backend..."
cd backend
python -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Create .env from example
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created backend/.env - Please add your API keys"
fi

cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
npm install

# Create .env.local from example
if [ ! -f .env.local ]; then
    cp .env.local.example .env.local
    echo "✅ Created frontend/.env.local"
fi

cd ..

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your OpenAI API key to backend/.env"
echo "2. Run: cd backend && source venv/bin/activate && python main.py"
echo "3. In another terminal: cd frontend && npm run dev"
echo "4. Open http://localhost:3000"
