#!/bin/bash

echo "======================================"
echo "  AeroBook - Flight Booking Platform"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example backend/.env
    echo "Please edit backend/.env with your configuration"
fi

# Initialize database
echo "Initializing database..."
cd backend
python3 << EOF
from app import create_app
from models import db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database initialized successfully!")
EOF

# Start the server
echo ""
echo "======================================"
echo "  Starting AeroBook Backend Server"
echo "======================================"
echo ""
echo "Backend API: http://localhost:5000"
echo "Frontend: Open frontend/index.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
