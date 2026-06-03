#!/bin/bash

# RAG Chatbot Start Script - Universal starter for development
# Usage: ./start.sh [backend|frontend|both]

set -e

COMMAND=${1:-both}

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_section() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if .env file exists
check_env() {
    if [ ! -f "$1/.env" ]; then
        print_warning "No .env file found in $1"
        if [ ! -f "$1/.env.example" ]; then
            echo "Error: .env.example not found"
            exit 1
        fi
        cp "$1/.env.example" "$1/.env"
        print_success "Created $1/.env from .env.example"
        echo "⚠️  Please update your API keys in $1/.env"
    fi
}

# Function to start backend
start_backend() {
    print_section "Starting RAG Chatbot Backend..."
    
    # Check if venv exists
    if [ ! -d "backend/venv" ]; then
        print_warning "Virtual environment not found. Creating..."
        cd backend
        python -m venv venv
        
        # Activate and install dependencies
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            source venv/Scripts/activate
        else
            source venv/bin/activate
        fi
        pip install -r requirements.txt
        cd ..
    fi
    
    # Check .env
    check_env backend
    
    # Start backend
    cd backend
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    print_success "Backend environment activated"
    print_section "Backend starting on http://localhost:8000"
    python main.py
}

# Function to start frontend
start_frontend() {
    print_section "Starting RAG Chatbot Frontend..."
    
    # Check if node_modules exists
    if [ ! -d "frontend/node_modules" ]; then
        print_warning "Dependencies not installed. Running npm install..."
        cd frontend
        npm install
        cd ..
    fi
    
    # Check .env.local
    if [ ! -f "frontend/.env.local" ]; then
        print_warning "No .env.local file found"
        if [ -f "frontend/.env.local.example" ]; then
            cp frontend/.env.local.example frontend/.env.local
            print_success "Created frontend/.env.local"
        fi
    fi
    
    # Start frontend
    cd frontend
    print_success "Frontend starting on http://localhost:3000"
    npm run dev
}

# Main logic
case $COMMAND in
    backend)
        start_backend
        ;;
    frontend)
        start_frontend
        ;;
    both)
        echo ""
        echo "╔══════════════════════════════════════════════════════════════╗"
        echo "║         🎥 RAG VIDEO CHATBOT - DEVELOPMENT SERVER             ║"
        echo "╚══════════════════════════════════════════════════════════════╝"
        echo ""
        print_warning "To run both services, open two terminals:"
        echo ""
        echo "Terminal 1 - Backend:"
        echo "  ./start.sh backend"
        echo ""
        echo "Terminal 2 - Frontend:"
        echo "  ./start.sh frontend"
        echo ""
        print_section "Starting Backend in new process..."
        start_backend &
        BACKEND_PID=$!
        sleep 3
        
        print_section "Starting Frontend in new process..."
        start_frontend &
        FRONTEND_PID=$!
        
        print_success "Both services started!"
        echo ""
        echo "📍 Frontend: http://localhost:3000"
        echo "📍 Backend:  http://localhost:8000"
        echo "📍 Docs:     http://localhost:8000/docs"
        echo ""
        print_warning "Press Ctrl+C to stop both services"
        
        # Wait for both processes
        wait
        ;;
    *)
        echo "Usage: $0 [backend|frontend|both]"
        echo ""
        echo "Examples:"
        echo "  $0 backend    # Start only backend"
        echo "  $0 frontend   # Start only frontend"
        echo "  $0 both       # Start both services (recommended for first time)"
        exit 1
        ;;
esac
