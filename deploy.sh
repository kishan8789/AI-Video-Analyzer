#!/bin/bash

# Production deployment script for RAG Chatbot
# Usage: ./deploy.sh prod

set -e

ENVIRONMENT=$1
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ -z "$ENVIRONMENT" ]; then
    echo "Usage: ./deploy.sh [prod|staging]"
    exit 1
fi

echo "🚀 Deploying to $ENVIRONMENT..."

# 1. Build Docker images
echo "📦 Building Docker images..."
docker-compose -f docker-compose.yml build

# 2. Push to registry (if configured)
if [ "$ENVIRONMENT" = "prod" ]; then
    echo "📤 Pushing to registry..."
    docker tag rag-chatbot-backend:latest registry.example.com/rag-chatbot-backend:$TIMESTAMP
    docker push registry.example.com/rag-chatbot-backend:$TIMESTAMP
fi

# 3. Deploy services
echo "🚀 Deploying services..."
docker-compose -f docker-compose.yml up -d

# 4. Run migrations/setup
echo "⚙️  Running setup..."
docker-compose -f docker-compose.yml exec -T backend python -c "from app.services.vector_store import VectorStoreService; VectorStoreService()"

# 5. Health checks
echo "✅ Running health checks..."
sleep 5
curl -f http://localhost:8000/api/health || exit 1
curl -f http://localhost:3000 || exit 1

# 6. Notify
echo "✨ Deployment successful!"
echo "Backend: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"
