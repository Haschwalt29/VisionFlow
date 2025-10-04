#!/bin/bash

# VisionFlow Setup Script
echo "🤖 Setting up VisionFlow: AI Workflow Automation Agent"
echo "======================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Python and Node.js found"

# Setup backend
echo "📦 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp env_example.txt .env
    echo "⚠️  Please edit backend/.env and add your OpenAI API key!"
fi

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "from database import init_db; init_db()"

echo "✅ Backend setup complete!"

# Setup frontend
cd ../frontend
echo "📦 Setting up frontend..."

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"

echo ""
echo "🎉 VisionFlow is ready to run!"
echo ""
echo "To start the demo:"
echo "1. Add your OpenAI API key to backend/.env"
echo "2. Run: python3 run_demo.py"
echo ""
echo "Or start manually:"
echo "1. Backend: cd backend && python3 app.py"
echo "2. Frontend: cd frontend && npm start"
echo ""
echo "🌐 Then visit: http://localhost:3000"
