@echo off
REM VisionFlow Setup Script for Windows

echo 🤖 Setting up VisionFlow: AI Workflow Automation Agent
echo ======================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✅ Python and Node.js found

REM Setup backend
echo 📦 Setting up backend...
cd backend

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy env_example.txt .env
    echo ⚠️  Please edit backend/.env and add your OpenAI API key!
)

REM Initialize database
echo 🗄️ Initializing database...
python -c "from database import init_db; init_db()"

echo ✅ Backend setup complete!

REM Setup frontend
cd ..\frontend
echo 📦 Setting up frontend...

REM Install Node.js dependencies
echo Installing Node.js dependencies...
npm install

echo ✅ Frontend setup complete!

echo.
echo 🎉 VisionFlow is ready to run!
echo.
echo To start the demo:
echo 1. Add your OpenAI API key to backend/.env
echo 2. Run: python run_demo.py
echo.
echo Or start manually:
echo 1. Backend: cd backend ^&^& python app.py
echo 2. Frontend: cd frontend ^&^& npm start
echo.
echo 🌐 Then visit: http://localhost:3000

pause
