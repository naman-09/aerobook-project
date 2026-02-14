from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(255))
    frequent_flyer_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    tickets = db.relationship('SupportTicket', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'address': self.address,
            'frequent_flyer_number': self.frequent_flyer_number,
            'created_at': self.created_at.isoformat()
        }

class Booking(db.Model):
    """Booking model for flight reservations"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    booking_reference = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    # Flight details
    flight_id = db.Column(db.String(50), nullable=False)
    airline = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.String(10), nullable=False)
    arrival_time = db.Column(db.String(10), nullable=False)
    departure_date = db.Column(db.Date, nullable=False, index=True)
    duration = db.Column(db.String(20))
    
    # Booking details
    passengers = db.Column(db.Integer, default=1)
    class_type = db.Column(db.String(20), default='economy')  # economy, business, first
    price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed', index=True)  # confirmed, cancelled, completed
    
    # Passenger information
    passenger_name = db.Column(db.String(100), nullable=False)
    passenger_email = db.Column(db.String(120), nullable=False)
    passenger_phone = db.Column(db.String(20), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert booking to dictionary"""
        return {
            'id': self.id,
            'booking_reference': self.booking_reference,
            'flight_id': self.flight_id,
            'airline': self.airline,
            'origin': self.origin,
            'destination': self.destination,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'departure_date': self.departure_date.isoformat(),
            'duration': self.duration,
            'passengers': self.passengers,
            'class_type': self.class_type,
            'price': self.price,
            'total_price': self.total_price,
            'status': self.status,
            'passenger_name': self.passenger_name,
            'passenger_email': self.passenger_email,
            'passenger_phone': self.passenger_phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class SupportTicket(db.Model):
    """Support ticket model"""
    __tablename__ = 'support_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium', index=True)  # low, medium, high, urgent
    status = db.Column(db.String(20), default='open', index=True)  # open, in_progress, resolved, closed
    
    booking_reference = db.Column(db.String(20))
    
    # Contact info for non-authenticated users
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(120))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert ticket to dictionary"""
        return {
            'id': self.id,
            'ticket_number': self.ticket_number,
            'subject': self.subject,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'booking_reference': self.booking_reference,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }

class Enquiry(db.Model):
    """Enquiry model for contact form submissions"""
    __tablename__ = 'enquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')  # new, read, responded
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert enquiry to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
