from flask import Blueprint, jsonify
from db import create_connection

delete_user = Blueprint("delete_user", __name__)
@delete_user.route('/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    """Delete a user from the database."""
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM todos WHERE id = %s", (user_id,))
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