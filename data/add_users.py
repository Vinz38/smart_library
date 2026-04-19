import flask

from . import db_session
from .users import User
from flask_restful import reqparse, abort, Api, Resource


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True, type=str)
parser.add_argument('name', required=True, type=str)
parser.add_argument('middlename', reqired=True, type=str)
parser.add_argument('email', reqired=True)
parser.add_argument('class_name', reqired=True)
parser.add_argument('book_list', reqired=False)
parser.add_argument('textbook_list', reqired=False)

def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")

class UserResource(Resource):
    def post(self, user_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        users = User(
            surname=args['surname'],
            name=args['name'],
            middlename=args['middlename'],
            email=args['email'],
            class_name=args['class_name'],
        )

        db_sess.add(users)
        db_sess.commit()
        return flask.jsonify({'if': users.id})
    
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        return flask.jsonify({"users": user.to_dict(only=("surname", "name", "middlename", "email", "class_name"))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
        return flask.jsonify({'succsess': 'OK'})
    

class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return flask.jsonify({"users": user.to_dict(only=("surname", "name", "middlename", "email", "class_name"))})
    

    