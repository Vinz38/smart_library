from data import db_session, add_users, register_lib
from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)

api.add(add_users.UserResource, 'api/add_user/<int:user_id>')
api.add(add_users.UserListResource, 'api/add_user')

@app.route('/main')
def main():
    return "OK"


if __name__ == "__main__":
    db_session.create_session("db/library.db")
    app.run(port=8080, host="127.0.0.1")