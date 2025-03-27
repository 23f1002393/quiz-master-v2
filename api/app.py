from database import *
from flask_cors import CORS
from config import AppConfig
from resources import api, jwt
from flask_restful import NotFound, MethodNotAllowed
from flask import Flask, make_response, jsonify, request
from flask_jwt_extended import unset_jwt_cookies, set_access_cookies, create_access_token
from werkzeug.security import check_password_hash
from sqlalchemy import select

cors = CORS()
def create_app():
    app = Flask(__name__)
    # add the API and AppConfig
    cors.init_app(app, supports_credentials=True)
    api.init_app(app)
    jwt.init_app(app)
    app.config.from_object(AppConfig)
    app.app_context().push()

    return app

# initialize the app
app = create_app()
# initialize the database
init_db(app)

@app.route('/login', methods=('POST',))
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if user := session.execute(select(User).where(User.email==email)).scalar():
        if check_password_hash(user.password, password):
            response = make_response({
                "id": user.id,
                "name": user.name, 
                "isAdmin": user.email=='admin@qm.xyz'
            })

            access_token = create_access_token(identity=user)
            set_access_cookies(response, access_token)
            return response
        return jsonify(message='invalid credentials'), 401
    return jsonify(message='failed to login user'), 404

@app.route('/logout', methods=('GET',))
def logout():
    response = make_response(message='user logged out')
    unset_jwt_cookies(response)
    return response, 200


@app.errorhandler(NotFound)
def handle_method_not_found(e):
    response = jsonify({"message": str(e)})
    response.status_code = 404
    return response


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    response = jsonify({"message": str(e)})
    response.status_code = 405
    return response


if __name__ == "__main__":
    app.run()
