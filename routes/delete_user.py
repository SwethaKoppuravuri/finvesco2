from flask import Blueprint, jsonify, request
from db import create_connection

delete_user = Blueprint("delete_user", __name__)
@delete_user.route('/delete', methods=['DELETE'])
def delete_user_route():
    """"Delete a user from the database based on query parameters."""
    name_filter = request.args.get('name')
    description_filter = request.args.get('description')
    id_filter = request.args.get('id')

    if not name_filter and not description_filter and not id_filter:
        return jsonify({'error': 'At least one filter parameter (name or description or id) must be provided'}), 400

    where_clauses = []
    values = []

    if name_filter:
        where_clauses.append("name = %s")
        values.append(name_filter)
    if description_filter:
        where_clauses.append("description = %s")
        values.append(description_filter)
    if id_filter:
        where_clauses.append("id = %s")
        values.append(id_filter)

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = f"DELETE FROM todos WHERE {' AND '.join(where_clauses)}"
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'User deleted successfully'}), 200
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'error': 'Failed to delete user'}), 500
    finally:
        cursor.close()
        connection.close()