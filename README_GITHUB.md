# ✈️ AeroBook - Professional Flight Booking Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A complete full-stack flight booking platform with Python Flask backend and React frontend**

[Features](#-features) • [Installation](#-installation) • [API Docs](#-api-endpoints) • [Tech Stack](#-technology-stack) • [Screenshots](#-screenshots)

</div>

---

## 📋 Project Overview

AeroBook is a comprehensive full-stack web application for searching, comparing, and booking flights worldwide. Built with **Python Flask** backend and **React** frontend, it provides a seamless user experience for travelers.

## 🎯 Key Highlights

- ✅ **Full-Stack Python Project** - Complete Flask REST API backend
- ✅ **Database Integration** - SQLAlchemy ORM with 4 data models
- ✅ **Authentication System** - JWT-based secure authentication
- ✅ **RESTful API** - 30+ documented API endpoints
- ✅ **Modern Frontend** - React with Tailwind CSS
- ✅ **Production Ready** - Complete with error handling and validation

## 🚀 Features

### Backend (Python Flask)
- **User Authentication**: JWT-based registration and login
- **Flight Search**: Intelligent flight search with filters
- **Booking Management**: Create, read, update, and cancel bookings
- **Support System**: Complete ticket management system
- **Profile Management**: User profile updates and password changes
- **Database Models**: 4 SQLAlchemy models with relationships

### Frontend (React)
- **Flight Search Interface**: Multi-criteria search
- **Booking Dashboard**: View and manage all bookings
- **User Profile**: Complete profile management
- **Support Center**: Multi-channel support with ticket creation
- **Responsive Design**: Mobile-first responsive layout
- **Legal Pages**: Privacy Policy and Terms of Service

## 🛠️ Technology Stack

### Backend
```
Python 3.10+
├── Flask 3.0          # Web Framework
├── SQLAlchemy 2.0     # ORM
├── Flask-JWT-Extended # Authentication
├── Flask-CORS         # Cross-Origin Resource Sharing
├── bcrypt             # Password Hashing
└── SQLite             # Database
```

### Frontend
```
React 18
├── Tailwind CSS       # Styling
├── JavaScript ES6+    # Programming
└── HTML5              # Structure
```

## 📁 Project Structure

```
aerobook-project/
├── backend/                  # Python Flask Backend
│   ├── app.py               # Main Flask application
│   ├── config.py            # Configuration settings
│   ├── models.py            # SQLAlchemy models
│   └── routes/              # API route handlers
│       ├── auth.py          # Authentication endpoints
│       ├── flights.py       # Flight search endpoints
│       ├── bookings.py      # Booking management
│       ├── support.py       # Support tickets
│       ├── profile.py       # User profile
│       └── enquiry.py       # Contact enquiries
├── frontend/                # React Frontend
│   └── index.html           # Single-page application
├── README.md                # This file
├── INSTALLATION.md          # Detailed setup guide
├── PROJECT_SUMMARY.md       # Complete project documentation
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitattributes           # Git language detection
└── run.sh                   # Quick start script
```

## 🔧 Installation

### Quick Start (Recommended)

**Linux/Mac:**
```bash
git clone https://github.com/yourusername/aerobook.git
cd aerobook
chmod +x run.sh
./run.sh
```

**Windows:**
```cmd
git clone https://github.com/yourusername/aerobook.git
cd aerobook
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd backend
python app.py
```

### Manual Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/aerobook.git
cd aerobook
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize database**
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

5. **Run the backend**
```bash
python app.py
```

Backend runs on `http://localhost:5000`

6. **Open frontend**

Open `frontend/index.html` in your browser or serve it:
```bash
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000`

## 🔌 API Endpoints

### Authentication
```http
POST   /api/auth/register    # Register new user
POST   /api/auth/login       # User login
GET    /api/auth/me          # Get current user
POST   /api/auth/logout      # Logout user
```

### Flights
```http
GET    /api/flights/search   # Search flights
GET    /api/flights/:id      # Get flight details
GET    /api/flights/airports # List all airports
```

### Bookings
```http
POST   /api/bookings               # Create booking
GET    /api/bookings               # Get user bookings
GET    /api/bookings/:id           # Get booking details
PUT    /api/bookings/:id           # Update booking
POST   /api/bookings/:id/cancel    # Cancel booking
GET    /api/bookings/reference/:ref # Lookup by reference
```

### Support
```http
POST   /api/support/tickets     # Create support ticket
GET    /api/support/tickets     # Get user tickets
GET    /api/support/tickets/:id # Get ticket details
PUT    /api/support/tickets/:id # Update ticket
GET    /api/support/faq         # Get FAQ items
```

### Profile
```http
GET    /api/profile          # Get user profile
PUT    /api/profile          # Update profile
PUT    /api/profile/password # Change password
```

### Enquiry
```http
POST   /api/enquiry       # Submit enquiry
GET    /api/enquiry/:id   # Get enquiry details
```

## 💾 Database Schema

### Models (SQLAlchemy)

**User**
- Authentication and profile information
- Relationships: bookings, support_tickets

**Booking**
- Flight reservations and passenger details
- Status tracking (confirmed, cancelled, completed)

**SupportTicket**
- Customer support tickets
- Priority levels and status tracking

**Enquiry**
- General contact form submissions

## 🔐 Security Features

- **Password Hashing**: bcrypt encryption
- **JWT Authentication**: Secure token-based auth
- **CORS Protection**: Cross-origin request security
- **SQL Injection Prevention**: SQLAlchemy ORM parameterization
- **Input Validation**: Server-side validation on all endpoints
- **Secure Sessions**: Token expiry and refresh mechanisms

## 🧪 Testing

Test the API endpoints:

```bash
# Health check
curl http://localhost:5000/api/health

# Search flights
curl "http://localhost:5000/api/flights/search?origin=New%20York%20(JFK)&destination=London%20(LHR)&date=2026-03-15&passengers=1"

# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'
```

## 📸 Screenshots

### Home - Flight Search
![Flight Search Interface](docs/screenshots/home.png)

### Flight Results
![Flight Results](docs/screenshots/results.png)

### My Bookings
![Booking Management](docs/screenshots/bookings.png)

### Support Center
![Support System](docs/screenshots/support.png)

## 🚀 Deployment

### Heroku
```bash
heroku create aerobook
git push heroku main
heroku open
```

### Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["python", "app.py"]
```

### Production Considerations
- Use PostgreSQL instead of SQLite
- Set up proper environment variables
- Enable HTTPS
- Configure CORS for specific domains
- Set up monitoring and logging

## 📝 Environment Variables

Copy `.env.example` to `.env` and configure:

```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=sqlite:///aerobook.db
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Flask and React
- Database management with SQLAlchemy
- Authentication with Flask-JWT-Extended
- UI styling with Tailwind CSS

## 📞 Support

For issues, questions, or contributions:
- **Email**: support@aerobook.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/aerobook/issues)
- **Documentation**: See [INSTALLATION.md](INSTALLATION.md) and [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

<div align="center">

**Built with ❤️ using Python Flask**

[⬆ Back to Top](#-aerobook---professional-flight-booking-platform)

</div>
