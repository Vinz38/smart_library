from data import db_session, add_users, register_lib, add_book
from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource
from dotenv import load_dotenv
import os 


load_dotenv()
api_key = os.getenv("API_KEY")


app = Flask(__name__)
app.config['SECRET_KEY'] = api_key
api = Api(app)

api.add_resource(add_users.UserResource, '/api/add_users/<int:user_id>')
api.add_resource(add_users.UserListResource, '/api/add_users')
api.add_resource(add_book.BookResourse, '/api/add_book/<int:book_id>')
api.add_resource(add_book.BookListResource, '/api/add_book')



@app.route('/main')
def main():
    return "OK"


if __name__ == "__main__":
    db_session.global_init("db/library.db")
    app.run(port=5050, host="127.0.0.1")