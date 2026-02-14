from flask import Blueprint, request, jsonify
import random
from datetime import datetime, timedelta

flights_bp = Blueprint('flights', __name__)

# Mock airlines data
AIRLINES = [
    {'name': 'SkyWings', 'code': 'SW', 'rating': 4.5},
    {'name': 'AeroElite', 'code': 'AE', 'rating': 4.7},
    {'name': 'CloudNine', 'code': 'CN', 'rating': 4.3},
    {'name': 'JetStream', 'code': 'JS', 'rating': 4.6},
    {'name': 'FlyHigh', 'code': 'FH', 'rating': 4.4},
    {'name': 'Pacific Air', 'code': 'PA', 'rating': 4.8},
    {'name': 'Continental Express', 'code': 'CE', 'rating': 4.2}
]

def generate_flight_data(origin, destination, date, passengers=1):
    """Generate mock flight data"""
    flights = []
    
    for i in range(8):
        airline = random.choice(AIRLINES)
        
        # Generate times
        dep_hour = 6 + (i * 2)
        dep_minute = random.choice([0, 30])
        departure_time = f"{dep_hour:02d}:{dep_minute:02d}"
        
        # Duration between 2-8 hours
        duration_hours = random.randint(2, 8)
        duration_minutes = random.choice([0, 15, 30, 45])
        duration = f"{duration_hours}h {duration_minutes}m"
        
        arr_hour = (dep_hour + duration_hours) % 24
        arr_minute = (dep_minute + duration_minutes) % 60
        arrival_time = f"{arr_hour:02d}:{arr_minute:02d}"
        
        # Price varies by distance and airline
        base_price = random.randint(150, 500)
        price = base_price + (passengers - 1) * (base_price * 0.8)
        
        flight = {
            'id': f"{airline['code']}{1000 + i}",
            'airline': airline['name'],
            'airline_code': airline['code'],
            'rating': airline['rating'],
            'origin': origin,
            'destination': destination,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'date': date,
            'duration': duration,
            'price': round(price, 2),
            'stops': random.choice([0, 0, 0, 1]),  # Mostly non-stop
            'seats_available': random.randint(10, 60),
            'aircraft': random.choice(['Boeing 737', 'Airbus A320', 'Boeing 787', 'Airbus A350'])
        }
        
        flights.append(flight)
    
    # Sort by price
    flights.sort(key=lambda x: x['price'])
    
    return flights

@flights_bp.route('/search', methods=['GET'])
def search_flights():
    """Search for flights"""
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')
    passengers = int(request.args.get('passengers', 1))
    class_type = request.args.get('class', 'economy')
    
    # Validate required parameters
    if not all([origin, destination, date]):
        return jsonify({'error': 'Origin, destination, and date are required'}), 400
    
    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Generate flight data
    flights = generate_flight_data(origin, destination, date, passengers)
    
    # Apply class pricing multiplier
    multiplier = {'economy': 1.0, 'business': 2.5, 'first': 4.0}.get(class_type, 1.0)
    for flight in flights:
        flight['price'] = round(flight['price'] * multiplier, 2)
        flight['class'] = class_type
    
    return jsonify({
        'flights': flights,
        'count': len(flights),
        'search_params': {
            'origin': origin,
            'destination': destination,
            'date': date,
            'passengers': passengers,
            'class': class_type
        }
    }), 200

@flights_bp.route('/<flight_id>', methods=['GET'])
def get_flight_details(flight_id):
    """Get details of a specific flight"""
    # In a real application, this would query a database
    # For now, return mock data
    
    airline_code = flight_id[:2]
    airline = next((a for a in AIRLINES if a['code'] == airline_code), AIRLINES[0])
    
    flight = {
        'id': flight_id,
        'airline': airline['name'],
        'airline_code': airline['code'],
        'rating': airline['rating'],
        'departure_time': '10:30',
        'arrival_time': '14:45',
        'duration': '4h 15m',
        'price': 299.99,
        'stops': 0,
        'seats_available': 24,
        'aircraft': 'Boeing 737',
        'amenities': ['WiFi', 'In-flight Entertainment', 'Meals', 'Extra Legroom'],
        'baggage': {
            'carry_on': '1 x 7kg',
            'checked': '2 x 23kg'
        }
    }
    
    return jsonify({'flight': flight}), 200

@flights_bp.route('/airports', methods=['GET'])
def get_airports():
    """Get list of available airports"""
    airports = [
        {'code': 'JFK', 'name': 'John F. Kennedy International', 'city': 'New York', 'country': 'USA'},
        {'code': 'LHR', 'name': 'London Heathrow', 'city': 'London', 'country': 'UK'},
        {'code': 'NRT', 'name': 'Narita International', 'city': 'Tokyo', 'country': 'Japan'},
        {'code': 'DXB', 'name': 'Dubai International', 'city': 'Dubai', 'country': 'UAE'},
        {'code': 'SIN', 'name': 'Singapore Changi', 'city': 'Singapore', 'country': 'Singapore'},
        {'code': 'CDG', 'name': 'Charles de Gaulle', 'city': 'Paris', 'country': 'France'},
        {'code': 'LAX', 'name': 'Los Angeles International', 'city': 'Los Angeles', 'country': 'USA'},
        {'code': 'SYD', 'name': 'Sydney Airport', 'city': 'Sydney', 'country': 'Australia'},
        {'code': 'HKG', 'name': 'Hong Kong International', 'city': 'Hong Kong', 'country': 'China'},
        {'code': 'FRA', 'name': 'Frankfurt Airport', 'city': 'Frankfurt', 'country': 'Germany'},
        {'code': 'YYZ', 'name': 'Toronto Pearson', 'city': 'Toronto', 'country': 'Canada'},
        {'code': 'BOM', 'name': 'Chhatrapati Shivaji Maharaj International', 'city': 'Mumbai', 'country': 'India'}
    ]
    
    return jsonify({'airports': airports}), 200
