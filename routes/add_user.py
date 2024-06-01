from flask import Blueprint, request, jsonify
from db import create_connection

add_user = Blueprint('add_user', __name__)


@add_user.route('/', methods=['POST'])
def add_user_route():
    """Add a new user to the database."""
    data = request.get_json()

    name = data['name']
    description = data['description']

    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO todos(name, description) VALUES (%s, %s)", (name, description))
        connection.commit()
        return jsonify({'message': 'User added successfully'}), 201
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'error': 'Failed to add user'}), 500
    finally:
        cursor.close()
        connection.close()