from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import db, SupportTicket
from datetime import datetime
import random
import string

support_bp = Blueprint('support', __name__)

def generate_ticket_number():
    """Generate unique ticket number"""
    return 'TKT' + ''.join(random.choices(string.digits, k=5))

@support_bp.route('/tickets', methods=['POST'])
def create_ticket():
    """Create a support ticket (auth optional)"""
    data = request.get_json()
    
    # Try to get user_id if authenticated
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except:
        pass
    
    # Validate required fields
    required_fields = ['subject', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # If not authenticated, require contact info
    if not user_id:
        if not data.get('contact_name') or not data.get('contact_email'):
            return jsonify({'error': 'Contact name and email required'}), 400
    
    # Generate ticket number
    ticket_num = generate_ticket_number()
    while SupportTicket.query.filter_by(ticket_number=ticket_num).first():
        ticket_num = generate_ticket_number()
    
    # Create ticket
    ticket = SupportTicket(
        user_id=user_id,
        ticket_number=ticket_num,
        subject=data['subject'],
        description=data['description'],
        priority=data.get('priority', 'medium'),
        booking_reference=data.get('booking_reference'),
        contact_name=data.get('contact_name'),
        contact_email=data.get('contact_email'),
        status='open'
    )
    
    try:
        db.session.add(ticket)
        db.session.commit()
        
        return jsonify({
            'message': 'Support ticket created successfully',
            'ticket': ticket.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Ticket creation failed'}), 500

@support_bp.route('/tickets', methods=['GET'])
@jwt_required()
def get_user_tickets():
    """Get all tickets for current user"""
    user_id = get_jwt_identity()
    
    # Get query parameters
    status = request.args.get('status')
    
    query = SupportTicket.query.filter_by(user_id=user_id)
    
    if status:
        query = query.filter_by(status=status)
    
    tickets = query.order_by(SupportTicket.created_at.desc()).all()
    
    return jsonify({
        'tickets': [ticket.to_dict() for ticket in tickets],
        'count': len(tickets)
    }), 200

@support_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
@jwt_required()
def get_ticket(ticket_id):
    """Get specific ticket details"""
    user_id = get_jwt_identity()
    
    ticket = SupportTicket.query.filter_by(id=ticket_id, user_id=user_id).first()
    
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    
    return jsonify({'ticket': ticket.to_dict()}), 200

@support_bp.route('/tickets/<int:ticket_id>', methods=['PUT'])
@jwt_required()
def update_ticket(ticket_id):
    """Update ticket (user can only update description)"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    ticket = SupportTicket.query.filter_by(id=ticket_id, user_id=user_id).first()
    
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    
    # Users can only update description and priority
    if 'description' in data:
        ticket.description = data['description']
    if 'priority' in data:
        ticket.priority = data['priority']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Ticket updated successfully',
            'ticket': ticket.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Update failed'}), 500

@support_bp.route('/tickets/number/<ticket_num>', methods=['GET'])
def get_ticket_by_number(ticket_num):
    """Get ticket by ticket number (no auth required for lookup)"""
    ticket = SupportTicket.query.filter_by(ticket_number=ticket_num).first()
    
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    
    return jsonify({'ticket': ticket.to_dict()}), 200

@support_bp.route('/faq', methods=['GET'])
def get_faq():
    """Get FAQ items"""
    faqs = [
        {
            'id': 1,
            'question': 'How do I cancel my booking?',
            'answer': 'You can cancel your booking from the "My Bookings" page. Click on the "Cancel Booking" button next to your reservation. Cancellation fees may apply based on the airline\'s policy.',
            'category': 'bookings'
        },
        {
            'id': 2,
            'question': 'What payment methods do you accept?',
            'answer': 'We accept all major credit cards (Visa, MasterCard, American Express), debit cards, and PayPal. All transactions are secured with 256-bit encryption.',
            'category': 'payments'
        },
        {
            'id': 3,
            'question': 'Can I change my flight date?',
            'answer': 'Yes, flight date changes are subject to availability and airline policies. Additional charges may apply. Contact our support team for assistance.',
            'category': 'bookings'
        },
        {
            'id': 4,
            'question': 'How early should I arrive at the airport?',
            'answer': 'We recommend arriving at least 2 hours before domestic flights and 3 hours before international flights to allow time for check-in and security procedures.',
            'category': 'travel'
        },
        {
            'id': 5,
            'question': 'What is your refund policy?',
            'answer': 'Refund policies vary by airline and ticket type. Fully refundable tickets can be cancelled with a full refund, while non-refundable tickets may incur cancellation fees.',
            'category': 'refunds'
        }
    ]
    
    category = request.args.get('category')
    if category:
        faqs = [faq for faq in faqs if faq['category'] == category]
    
    return jsonify({'faqs': faqs, 'count': len(faqs)}), 200
