@echo off
REM RAG Chatbot Start Script for Windows
REM Usage: start.bat [backend|frontend|both]

setlocal enabledelayedexpansion

set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=both

REM Function to check and create .env files
if not exist "backend\.env" (
    if exist "backend\.env.example" (
        copy backend\.env.example backend\.env
        echo.
        echo ⚠️  Created backend\.env - Please update with your API keys
        echo.
    )
)

if not exist "frontend\.env.local" (
    if exist "frontend\.env.local.example" (
        copy frontend\.env.local.example frontend\.env.local
        echo.
        echo ✅ Created frontend\.env.local
        echo.
    )
)

REM Main logic
if "%COMMAND%"=="backend" (
    call :start_backend
) else if "%COMMAND%"=="frontend" (
    call :start_frontend
) else if "%COMMAND%"=="both" (
    call :start_both
) else (
    echo Usage: start.bat [backend^|frontend^|both]
    echo.
    echo Examples:
    echo   start.bat backend    # Start only backend
    echo   start.bat frontend   # Start only frontend
    echo   start.bat both       # Start both services
    exit /b 1
)
goto :end

:start_backend
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║      🎥 RAG VIDEO CHATBOT - BACKEND SERVER                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if venv exists
if not exist "backend\venv" (
    echo ⚠️  Virtual environment not found. Creating...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    cd ..
)

echo ✅ Activating backend environment...
cd backend
call venv\Scripts\activate.bat
echo ✅ Backend environment activated

echo.
echo ▶ Backend starting on http://localhost:8000
echo.
python main.py
goto :end

:start_frontend
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║      🎥 RAG VIDEO CHATBOT - FRONTEND SERVER                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if node_modules exists
if not exist "frontend\node_modules" (
    echo ⚠️  Dependencies not installed. Running npm install...
    cd frontend
    call npm install
    cd ..
)

echo ✅ Starting frontend...
cd frontend
echo.
echo ▶ Frontend starting on http://localhost:3000
echo.
call npm run dev
goto :end

:start_both
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║      🎥 RAG VIDEO CHATBOT - DEVELOPMENT SERVER               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  To run both services, open TWO separate Command Prompts:
echo.
echo Command Prompt 1 - Backend:
echo   start.bat backend
echo.
echo Command Prompt 2 - Frontend:
echo   start.bat frontend
echo.
echo Or use your IDE's terminal features to run both in parallel.
echo.
echo.
echo 📍 Frontend: http://localhost:3000
echo 📍 Backend:  http://localhost:8000
echo 📍 Docs:     http://localhost:8000/docs
echo.
pause
goto :end

:end
endlocal
