from flask import Blueprint, request, jsonify
from db import create_connection

update_user = Blueprint('update_user', __name__)

@update_user.route('/update', methods=['PATCH'])
def update_user_route():
    """Update an existing user in the database based on query parameters."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    name_filter = request.args.get('name')
    id_filter = request.args.get('id')
    description_filter = request.args.get('description')

    if not name_filter and not description_filter and not id_filter:
        return jsonify({'error': 'At least one filter parameter (name or description or id) must be provided'}), 400

    fields = []
    values = []

    if 'name' in data:
        fields.append("name = %s")
        values.append(data['name'])
    if 'description' in data:
        fields.append("description = %s")
        values.append(data['description'])
    if 'id' in data:
        fields.append("id = %s")
        values.append(data['id'])

    if not fields:
        return jsonify({'error': 'No fields to update'}), 400

    where_clauses = []
    where_values = []

    if name_filter:
        where_clauses.append("name = %s")
        where_values.append(name_filter)
    if description_filter:
        where_clauses.append("description = %s")
        where_values.append(description_filter)
    if id_filter:
        where_clauses.append("id = %s")
        where_values.append((id_filter))

    values.extend(where_values)

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = f"UPDATE todos SET {', '.join(fields)} WHERE {' AND '.join(where_clauses)}"
        cursor.execute(query, values)
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