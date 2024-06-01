from flask import Blueprint, jsonify, request
from db import create_connection

get_users = Blueprint('get_users', __name__)

@get_users.route('/', methods=['GET'])
def get_users_route():
    """Fetch all users from the database."""
    name_filter = request.args.get('name')
    description_filter = request.args.get('description')
    id_filter = request.args.get('id')

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    base_query = "SELECT * FROM todos"
    filters = []
    values = []

    if name_filter:
        filters.append("name = %s")
        values.append(name_filter)
    if description_filter:
        filters.append("description = %s")
        values.append(description_filter)
    if id_filter:
        filters.append("id = %s")
        values.append(id_filter)

    if filters:
        query = f"{base_query} WHERE {' AND '.join(filters)}"
    else:
        query = base_query

    cursor.execute(query, values)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(rows)

