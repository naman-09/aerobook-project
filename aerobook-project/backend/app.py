from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db
import os

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.flights import flights_bp
    from routes.bookings import bookings_bp
    from routes.support import support_bp
    from routes.profile import profile_bp
    from routes.enquiry import enquiry_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(flights_bp, url_prefix='/api/flights')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(support_bp, url_prefix='/api/support')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(enquiry_bp, url_prefix='/api/enquiry')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'AeroBook API is running'
        })
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to AeroBook API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'flights': '/api/flights',
                'bookings': '/api/bookings',
                'support': '/api/support',
                'profile': '/api/profile',
                'enquiry': '/api/enquiry'
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
