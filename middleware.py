# middleware.py
from flask import request, jsonify

def validate_user_data():
    """Middleware to validate user data."""
    if request.method in ['POST', 'PATCH', 'DELETE']:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid input, no data provided'}), 400

        # Enforce NOT NULL constraints for POST and PATCH
        if request.method in ['POST', 'PATCH']:
            required_fields = ['id', 'name', 'description']
            for field in required_fields:
                if field not in data or data[field] is None or data[field] == '':
                    return jsonify({'error': f"'{field}' is required and cannot be null or empty"}), 400
    return None