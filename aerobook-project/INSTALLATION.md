# AeroBook Installation Guide

## Quick Start

### For Linux/Mac:

```bash
chmod +x run.sh
./run.sh
```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Initialize the database
- Start the backend server

### For Windows:

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd backend
python app.py
```

Then open `frontend/index.html` in your browser.

## Manual Installation

### Step 1: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

Copy `.env.example` to `backend/.env` and update the values:

```bash
cp .env.example backend/.env
```

Edit `backend/.env` with your preferred settings.

### Step 4: Initialize Database

```bash
cd backend
python3
>>> from app import create_app
>>> from models import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Step 5: Run Backend Server

```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Step 6: Open Frontend

Open `frontend/index.html` in your web browser.

Alternatively, serve it using Python's HTTP server:

```bash
cd frontend
python -m http.server 8000
```

Then navigate to `http://localhost:8000`

## Verification

### Test the API

```bash
curl http://localhost:5000/api/health
```

You should see:
```json
{
  "status": "healthy",
  "message": "AeroBook API is running"
}
```

### Test Flight Search

```bash
curl "http://localhost:5000/api/flights/search?origin=New%20York%20(JFK)&destination=London%20(LHR)&date=2026-03-15&passengers=1"
```

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, you can change it in `backend/app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

### Database Errors

Delete the existing database and recreate:

```bash
rm backend/aerobook.db
# Then run Step 4 again
```

### Module Not Found Errors

Ensure you're in the virtual environment:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Development

### Running Tests

```bash
pytest tests/
```

### Database Migrations

When you modify models:

```bash
cd backend
python manage.py db migrate
python manage.py db upgrade
```

### API Documentation

Visit `http://localhost:5000/` for API endpoint information.

## Production Deployment

### Using Gunicorn (Linux/Mac)

```bash
pip install gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Waitress (Windows)

```bash
pip install waitress
cd backend
waitress-serve --port=5000 app:app
```

### Environment Variables for Production

Update `backend/.env`:

```
FLASK_ENV=production
SECRET_KEY=your-very-secure-random-key
JWT_SECRET_KEY=your-very-secure-jwt-key
```

## Support

For issues or questions:
- Email: support@aerobook.com
- Create an issue in the repository
- Check the FAQ in README.md
