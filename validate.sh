#!/bin/bash

# Project validation script - checks if all components are in place

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
PASSED=0
FAILED=0
WARNINGS=0

print_check() {
    echo -e "${BLUE}▶ Checking: $1${NC}"
}

print_pass() {
    echo -e "${GREEN}✅ PASS: $1${NC}"
    ((PASSED++))
}

print_fail() {
    echo -e "${RED}❌ FAIL: $1${NC}"
    ((FAILED++))
}

print_warn() {
    echo -e "${YELLOW}⚠️  WARN: $1${NC}"
    ((WARNINGS++))
}

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║       RAG CHATBOT PROJECT VALIDATION SCRIPT                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# PROJECT STRUCTURE CHECKS
# ============================================================================
echo "📋 Checking Project Structure..."
echo ""

print_check "Backend directory structure"
if [ -d "backend/app/api" ] && [ -d "backend/app/services" ] && [ -d "backend/app/utils" ]; then
    print_pass "Backend app directories exist"
else
    print_fail "Backend app directories missing"
fi

print_check "Frontend directory structure"
if [ -d "frontend/src/app" ] && [ -d "frontend/src/components" ]; then
    print_pass "Frontend app directories exist"
else
    print_fail "Frontend app directories missing"
fi

# ============================================================================
# CONFIGURATION FILES
# ============================================================================
echo ""
echo "⚙️  Checking Configuration Files..."
echo ""

print_check ".env files"
if [ -f "backend/.env" ]; then
    print_pass "backend/.env exists"
else
    print_warn "backend/.env not found (will be created on first setup)"
fi

if [ -f "backend/.env.example" ]; then
    print_pass "backend/.env.example exists"
else
    print_fail "backend/.env.example missing"
fi

if [ -f "frontend/.env.local" ]; then
    print_pass "frontend/.env.local exists"
else
    print_warn "frontend/.env.local not found (will be created on first setup)"
fi

if [ -f "frontend/.env.local.example" ]; then
    print_pass "frontend/.env.local.example exists"
else
    print_fail "frontend/.env.local.example missing"
fi

print_check "Docker configuration"
if [ -f "docker-compose.yml" ]; then
    print_pass "docker-compose.yml exists"
else
    print_fail "docker-compose.yml missing"
fi

# ============================================================================
# PYTHON BACKEND FILES
# ============================================================================
echo ""
echo "🐍 Checking Python Backend Files..."
echo ""

BACKEND_FILES=(
    "backend/main.py"
    "backend/config.py"
    "backend/requirements.txt"
    "backend/app/__init__.py"
    "backend/app/models.py"
    "backend/app/api/__init__.py"
    "backend/app/api/routes.py"
    "backend/app/services/__init__.py"
    "backend/app/services/video_fetcher.py"
    "backend/app/services/vector_store.py"
    "backend/app/services/rag_pipeline.py"
    "backend/app/services/memory.py"
    "backend/app/services/social_apis.py"
    "backend/app/utils/__init__.py"
    "backend/app/utils/helpers.py"
    "backend/app/utils/streaming.py"
)

for file in "${BACKEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_pass "$file"
    else
        print_fail "$file missing"
    fi
done

# ============================================================================
# TYPESCRIPT/REACT FRONTEND FILES
# ============================================================================
echo ""
echo "⚛️  Checking React/Next.js Frontend Files..."
echo ""

FRONTEND_FILES=(
    "frontend/package.json"
    "frontend/tsconfig.json"
    "frontend/next.config.ts"
    "frontend/tailwind.config.ts"
    "frontend/postcss.config.js"
    "frontend/src/app/layout.tsx"
    "frontend/src/app/page.tsx"
    "frontend/src/app/globals.css"
    "frontend/src/components/ChatPanel.tsx"
    "frontend/src/components/URLInput.tsx"
    "frontend/src/components/VideoCards.tsx"
)

for file in "${FRONTEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_pass "$file"
    else
        print_fail "$file missing"
    fi
done

# ============================================================================
# SCRIPT FILES
# ============================================================================
echo ""
echo "🔧 Checking Script Files..."
echo ""

SCRIPT_FILES=(
    "setup.sh"
    "setup.bat"
    "start.sh"
    "start.bat"
    "deploy.sh"
)

for file in "${SCRIPT_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_pass "$file"
    else
        print_fail "$file missing"
    fi
done

# ============================================================================
# DOCUMENTATION FILES
# ============================================================================
echo ""
echo "📚 Checking Documentation..."
echo ""

if [ -f "README.md" ]; then
    # Check if README has key sections
    if grep -q "Quick Start" README.md && grep -q "Technology Stack" README.md; then
        print_pass "README.md is comprehensive"
    else
        print_warn "README.md exists but may be incomplete"
    fi
else
    print_fail "README.md missing"
fi

if [ -f ".gitignore" ]; then
    print_pass ".gitignore exists"
else
    print_warn ".gitignore not found"
fi

# ============================================================================
# DEPENDENCY CHECKS
# ============================================================================
echo ""
echo "📦 Checking Dependencies..."
echo ""

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_pass "Python installed: $PYTHON_VERSION"
    
    if [[ "$PYTHON_VERSION" > "3.10" ]]; then
        print_pass "Python version is 3.11+ (required)"
    else
        print_warn "Python version is older than 3.11 (recommended)"
    fi
else
    print_fail "Python 3 not found in PATH"
fi

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_pass "Node.js installed: $NODE_VERSION"
else
    print_fail "Node.js not found in PATH"
fi

if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_pass "npm installed: $NPM_VERSION"
else
    print_fail "npm not found in PATH"
fi

if command -v docker &> /dev/null; then
    print_pass "Docker installed"
else
    print_warn "Docker not installed (optional for development)"
fi

# ============================================================================
# PYTHON PACKAGE CHECKS
# ============================================================================
echo ""
echo "🐍 Checking Python Packages in requirements.txt..."
echo ""

REQUIRED_PACKAGES=(
    "fastapi"
    "uvicorn"
    "openai"
    "langchain"
    "chromadb"
    "youtube-transcript-api"
    "yt-dlp"
    "pydantic"
)

if [ -f "backend/requirements.txt" ]; then
    for package in "${REQUIRED_PACKAGES[@]}"; do
        if grep -q "$package" backend/requirements.txt; then
            print_pass "$package in requirements.txt"
        else
            print_fail "$package NOT in requirements.txt"
        fi
    done
else
    print_fail "requirements.txt not found"
fi

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    VALIDATION SUMMARY                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ PASSED: $PASSED${NC}"
echo -e "${YELLOW}⚠️  WARNINGS: $WARNINGS${NC}"
echo -e "${RED}❌ FAILED: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All critical checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./start.sh backend   (in terminal 1)"
    echo "2. Run: ./start.sh frontend  (in terminal 2)"
    echo "3. Open: http://localhost:3000"
    echo ""
else
    echo -e "${RED}⚠️  Some critical files are missing. Please run setup:${NC}"
    echo ""
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "   setup.bat"
    else
        echo "   chmod +x setup.sh && ./setup.sh"
    fi
    echo ""
fi
