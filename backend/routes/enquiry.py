from flask import Blueprint, request, jsonify
from models import db, Enquiry

enquiry_bp = Blueprint('enquiry', __name__)

@enquiry_bp.route('', methods=['POST'])
def submit_enquiry():
    """Submit a general enquiry"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Create enquiry
    enquiry = Enquiry(
        name=data['name'],
        email=data['email'],
        subject=data['subject'],
        message=data['message'],
        status='new'
    )
    
    try:
        db.session.add(enquiry)
        db.session.commit()
        
        return jsonify({
            'message': 'Enquiry submitted successfully',
            'enquiry': enquiry.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Submission failed'}), 500

@enquiry_bp.route('/<int:enquiry_id>', methods=['GET'])
def get_enquiry(enquiry_id):
    """Get enquiry details (for admin or tracking purposes)"""
    enquiry = Enquiry.query.get(enquiry_id)
    
    if not enquiry:
        return jsonify({'error': 'Enquiry not found'}), 404
    
    return jsonify({'enquiry': enquiry.to_dict()}), 200
