import flask

from data import db_session
from data.users import User
from flask_restful import reqparse, abort, Api, Resource


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True, type=str)
parser.add_argument('name', required=True, type=str)
parser.add_argument('middlename', required=True, type=str)
parser.add_argument('email', required=True)
parser.add_argument('class_name', required=True)
parser.add_argument('book_list', type=dict, required=False)
parser.add_argument('textbook_list', type=dict, required=False)

def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def put(self, user_id):
        abort_if_news_not_found(user_id)
        args = parser.parse_args()
        db_sess = db_session.create_session()

        user = db_sess.get(User, user_id)

        user.surname = args['surname']
        user.name = args['name']
        user.middlename = args['middlename']
        user.email = args['email']
        user.class_name = args['class_name']
        user.book_list = args.get('book_list')
        user.textbook_list = args.get('textbook_list')

        db_sess.commit()
        return flask.jsonify({'success': 'OK'})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.get(User, user_id)
        db_sess.delete(user)
        db_sess.commit()
        return flask.jsonify({'succsess': 'OK'})


class UserListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        user = db_sess.query(User).all()
        return [
            item.to_dict(only=(
                "surname",
                "name",
                "middlename",
                "email",
                "class_name",
                "book_list",
                "textbook_list"
            ))
            for item in user
        ]

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        users = User(
            surname=args['surname'],
            name=args['name'],
            middlename=args['middlename'],
            email=args['email'],
            class_name=args['class_name']
        )

        db_sess.add(users)
        db_sess.commit()
        return flask.jsonify({'succsess': 'OK'})
