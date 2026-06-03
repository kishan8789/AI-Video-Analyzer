@echo off
REM Project validation script for Windows

setlocal enabledelayedexpansion

set PASSED=0
set FAILED=0
set WARNINGS=0

cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║       RAG CHATBOT PROJECT VALIDATION SCRIPT                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM ============================================================================
REM PROJECT STRUCTURE CHECKS
REM ============================================================================
echo 📋 Checking Project Structure...
echo.

if exist "backend\app\api" (
    if exist "backend\app\services" (
        if exist "backend\app\utils" (
            echo ✅ PASS: Backend app directories exist
            set /a PASSED+=1
        ) else (
            echo ❌ FAIL: Backend app directories missing
            set /a FAILED+=1
        )
    ) else (
        echo ❌ FAIL: Backend app directories missing
        set /a FAILED+=1
    )
) else (
    echo ❌ FAIL: Backend app directories missing
    set /a FAILED+=1
)

if exist "frontend\src\app" (
    if exist "frontend\src\components" (
        echo ✅ PASS: Frontend app directories exist
        set /a PASSED+=1
    ) else (
        echo ❌ FAIL: Frontend app directories missing
        set /a FAILED+=1
    )
) else (
    echo ❌ FAIL: Frontend app directories missing
    set /a FAILED+=1
)

REM ============================================================================
REM CONFIGURATION FILES
REM ============================================================================
echo.
echo ⚙️  Checking Configuration Files...
echo.

if exist "backend\.env.example" (
    echo ✅ PASS: backend\.env.example exists
    set /a PASSED+=1
) else (
    echo ❌ FAIL: backend\.env.example missing
    set /a FAILED+=1
)

if exist "frontend\.env.local.example" (
    echo ✅ PASS: frontend\.env.local.example exists
    set /a PASSED+=1
) else (
    echo ❌ FAIL: frontend\.env.local.example missing
    set /a FAILED+=1
)

if exist "docker-compose.yml" (
    echo ✅ PASS: docker-compose.yml exists
    set /a PASSED+=1
) else (
    echo ❌ FAIL: docker-compose.yml missing
    set /a FAILED+=1
)

REM ============================================================================
REM PYTHON BACKEND FILES
REM ============================================================================
echo.
echo 🐍 Checking Python Backend Files...
echo.

set "BACKEND_FILES=backend\main.py backend\config.py backend\requirements.txt backend\app\__init__.py backend\app\models.py backend\app\api\__init__.py backend\app\api\routes.py backend\app\services\__init__.py backend\app\services\video_fetcher.py backend\app\services\vector_store.py backend\app\services\rag_pipeline.py backend\app\services\memory.py backend\app\services\social_apis.py backend\app\utils\__init__.py backend\app\utils\helpers.py backend\app\utils\streaming.py"

for %%F in (%BACKEND_FILES%) do (
    if exist "%%F" (
        echo ✅ PASS: %%F
        set /a PASSED+=1
    ) else (
        echo ❌ FAIL: %%F missing
        set /a FAILED+=1
    )
)

REM ============================================================================
REM TYPESCRIPT/REACT FRONTEND FILES
REM ============================================================================
echo.
echo ⚛️  Checking React/Next.js Frontend Files...
echo.

set "FRONTEND_FILES=frontend\package.json frontend\tsconfig.json frontend\next.config.ts frontend\tailwind.config.ts frontend\postcss.config.js frontend\src\app\layout.tsx frontend\src\app\page.tsx frontend\src\app\globals.css frontend\src\components\ChatPanel.tsx frontend\src\components\URLInput.tsx frontend\src\components\VideoCards.tsx"

for %%F in (%FRONTEND_FILES%) do (
    if exist "%%F" (
        echo ✅ PASS: %%F
        set /a PASSED+=1
    ) else (
        echo ❌ FAIL: %%F missing
        set /a FAILED+=1
    )
)

REM ============================================================================
REM SCRIPT FILES
REM ============================================================================
echo.
echo 🔧 Checking Script Files...
echo.

set "SCRIPT_FILES=setup.bat start.bat deploy.sh setup.sh start.sh"

for %%F in (%SCRIPT_FILES%) do (
    if exist "%%F" (
        echo ✅ PASS: %%F
        set /a PASSED+=1
    ) else (
        echo ❌ FAIL: %%F missing
        set /a FAILED+=1
    )
)

REM ============================================================================
REM DOCUMENTATION FILES
REM ============================================================================
echo.
echo 📚 Checking Documentation...
echo.

if exist "README.md" (
    echo ✅ PASS: README.md exists
    set /a PASSED+=1
) else (
    echo ❌ FAIL: README.md missing
    set /a FAILED+=1
)

if exist ".gitignore" (
    echo ✅ PASS: .gitignore exists
    set /a PASSED+=1
) else (
    echo ⚠️  WARN: .gitignore not found
    set /a WARNINGS+=1
)

REM ============================================================================
REM DEPENDENCY CHECKS
REM ============================================================================
echo.
echo 📦 Checking Dependencies...
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ PASS: Python installed: !PYTHON_VERSION!
    set /a PASSED+=1
) else (
    echo ❌ FAIL: Python not found
    set /a FAILED+=1
)

node --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✅ PASS: Node.js installed: !NODE_VERSION!
    set /a PASSED+=1
) else (
    echo ❌ FAIL: Node.js not found
    set /a FAILED+=1
)

npm --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f %%i in ('npm --version') do set NPM_VERSION=%%i
    echo ✅ PASS: npm installed: !NPM_VERSION!
    set /a PASSED+=1
) else (
    echo ❌ FAIL: npm not found
    set /a FAILED+=1
)

docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PASS: Docker installed
    set /a PASSED+=1
) else (
    echo ⚠️  WARN: Docker not installed (optional for development)
    set /a WARNINGS+=1
)

REM ============================================================================
REM SUMMARY
REM ============================================================================
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    VALIDATION SUMMARY                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ✅ PASSED: !PASSED!
echo ⚠️  WARNINGS: !WARNINGS!
echo ❌ FAILED: !FAILED!
echo.

if !FAILED! equ 0 (
    echo 🎉 All critical checks passed!
    echo.
    echo Next steps:
    echo 1. Run: start.bat backend   (in Command Prompt 1)
    echo 2. Run: start.bat frontend  (in Command Prompt 2)
    echo 3. Open: http://localhost:3000
    echo.
) else (
    echo ⚠️  Some critical files are missing. Please run setup:
    echo.
    echo    setup.bat
    echo.
)

pause
endlocal
