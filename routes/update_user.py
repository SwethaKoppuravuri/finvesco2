from flask import Blueprint, request, jsonify
from db import create_connection

update_user = Blueprint('update_user', __name__)

@update_user.route('/<int:user_id>', methods=['PATCH'])
def update_user_route(user_id):
    """Update an existing user in the database."""
    data = request.get_json()

    fields = []
    values = []

    if 'name' in data:
        fields.append("name = %s")
        values.append(data['name'])
    if 'description' in data:
        fields.append("description = %s")
        values.append(data['description'])


    if not fields:
        return jsonify({'error': 'No fields to update'}), 400

    values.append(user_id)

    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(f"UPDATE todos SET {', '.join(fields)} WHERE id = %s", values)
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'User updated successfully'}), 200
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'error': 'Failed to update user'}), 500
    finally:
        cursor.close()
        connection.close()