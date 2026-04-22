from data import db_session
from flask_restful_MODELS import flask_restful_model_CLASS, flask_restful_model_BOOK, flask_restful_model_LIBRARIAN, flask_restful_model_TEXTBOOK, flask_restful_model_USER
from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource
from dotenv import load_dotenv
import os 


load_dotenv()
api_key = os.getenv("API_KEY")


app = Flask(__name__)
app.config['SECRET_KEY'] = api_key
api = Api(app)

api.add_resource(flask_restful_model_USER.UserResource, '/api/users/<int:user_id>')
api.add_resource(flask_restful_model_USER.UserListResource, '/api/users')
api.add_resource(flask_restful_model_BOOK.BookResourse, '/api/book/<int:book_id>')
api.add_resource(flask_restful_model_BOOK.BookListResource, '/api/book')
api.add_resource(flask_restful_model_TEXTBOOK.TextBookResource, '/api/textbook/<int:textbook_id>')
api.add_resource(flask_restful_model_TEXTBOOK.TextBookListResource, '/api/textbook')
api.add_resource(flask_restful_model_LIBRARIAN.LibrarianListResource, '/api/librarian')
api.add_resource(flask_restful_model_CLASS.ClassResource, '/api/class')
print(app.url_map)

if __name__ == "__main__":
    db_session.global_init("db/library.db")
    app.run(port=8080, host="127.0.0.1")