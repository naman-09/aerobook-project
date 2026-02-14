from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Booking, User
from datetime import datetime
import random
import string

bookings_bp = Blueprint('bookings', __name__)

def generate_booking_reference():
    """Generate unique booking reference"""
    return 'BK' + ''.join(random.choices(string.digits, k=6))

@bookings_bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    """Create a new flight booking"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['flight_id', 'airline', 'origin', 'destination', 
                      'departure_time', 'arrival_time', 'departure_date',
                      'passengers', 'class_type', 'price', 'passenger_name',
                      'passenger_email', 'passenger_phone']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Generate booking reference
    booking_ref = generate_booking_reference()
    while Booking.query.filter_by(booking_reference=booking_ref).first():
        booking_ref = generate_booking_reference()
    
    # Parse date
    try:
        dep_date = datetime.strptime(data['departure_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Calculate total price
    price_per_person = float(data['price'])
    passengers = int(data['passengers'])
    total_price = price_per_person * passengers
    
    # Create booking
    booking = Booking(
        user_id=user_id,
        booking_reference=booking_ref,
        flight_id=data['flight_id'],
        airline=data['airline'],
        origin=data['origin'],
        destination=data['destination'],
        departure_time=data['departure_time'],
        arrival_time=data['arrival_time'],
        departure_date=dep_date,
        duration=data.get('duration', ''),
        passengers=passengers,
        class_type=data['class_type'],
        price=price_per_person,
        total_price=total_price,
        passenger_name=data['passenger_name'],
        passenger_email=data['passenger_email'],
        passenger_phone=data['passenger_phone'],
        status='confirmed'
    )
    
    try:
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Booking creation failed'}), 500

@bookings_bp.route('', methods=['GET'])
@jwt_required()
def get_user_bookings():
    """Get all bookings for current user"""
    user_id = get_jwt_identity()
    
    # Get query parameters for filtering
    status = request.args.get('status')
    
    query = Booking.query.filter_by(user_id=user_id)
    
    if status:
        query = query.filter_by(status=status)
    
    bookings = query.order_by(Booking.created_at.desc()).all()
    
    return jsonify({
        'bookings': [booking.to_dict() for booking in bookings],
        'count': len(bookings)
    }), 200

@bookings_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get specific booking details"""
    user_id = get_jwt_identity()
    
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    return jsonify({'booking': booking.to_dict()}), 200

@bookings_bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking(booking_id):
    """Update booking details"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Only allow updating certain fields
    allowed_fields = ['passenger_name', 'passenger_email', 'passenger_phone']
    
    for field in allowed_fields:
        if field in data:
            setattr(booking, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Booking updated successfully',
            'booking': booking.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Update failed'}), 500

@bookings_bp.route('/<int:booking_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking"""
    user_id = get_jwt_identity()
    
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.status == 'cancelled':
        return jsonify({'error': 'Booking already cancelled'}), 400
    
    booking.status = 'cancelled'
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Booking cancelled successfully',
            'booking': booking.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Cancellation failed'}), 500

@bookings_bp.route('/reference/<booking_ref>', methods=['GET'])
def get_booking_by_reference(booking_ref):
    """Get booking by reference number (no auth required for lookup)"""
    booking = Booking.query.filter_by(booking_reference=booking_ref).first()
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    return jsonify({'booking': booking.to_dict()}), 200
