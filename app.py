from flask import Flask, request
from routes.get_users import get_users
from routes.add_user import add_user
from routes.update_user import update_user
from routes.delete_user import delete_user
from middleware import validate_user_data
app = Flask(__name__)

@app.before_request
def before_request():
    if request.endpoint in ['app.get_users', 'app.add_user', 'app.update_user', 'app.delete_user']:
        error_response = validate_user_data()
        if error_response:
            return error_response


# Register blueprints
app.register_blueprint(get_users)
app.register_blueprint(add_user)
app.register_blueprint(update_user)
app.register_blueprint(delete_user)

if __name__ == '__main__':
    app.run(port=4000)

