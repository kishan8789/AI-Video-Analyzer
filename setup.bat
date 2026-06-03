# @echo off
REM Setup script for RAG Chatbot on Windows

echo.
echo 🚀 Setting up RAG Chatbot...
echo.

REM Backend setup
echo 📦 Setting up backend...
cd backend
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Create .env from example
if not exist .env (
    copy .env.example .env
    echo ✅ Created backend\.env - Please add your API keys
)

cd ..

REM Frontend setup
echo 📦 Setting up frontend...
cd frontend
call npm install

REM Create .env.local from example
if not exist .env.local (
    copy .env.local.example .env.local
    echo ✅ Created frontend\.env.local
)

cd ..

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Add your OpenAI API key to backend\.env
echo 2. Run: cd backend ^&^& venv\Scripts\activate.bat ^&^& python main.py
echo 3. In another terminal: cd frontend ^&^& npm run dev
echo 4. Open http://localhost:3000
echo.
pause
