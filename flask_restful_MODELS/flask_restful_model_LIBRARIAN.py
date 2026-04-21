import flask

from data import db_session
from data.librarians import Librarian

from flask_restful import reqparse, abort, Api, Resource

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True, type=str)
parser.add_argument('name', required=True, type=str)
parser.add_argument('middlename', required=True, type=str)
parser.add_argument('phonenumber', required=True)
parser.add_argument('hashed_password', required=True)


class LibrarianListResource(Resource):
    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        librarian = Librarian(
            surname=args['surname'],
            name=args['name'],
            middlename=args['middlename'],
            email=args['email'],
            phonenumber=args['phonenumber'],
        )

        librarian.set_password(args['hashed_password'])
        db_sess.add(librarian)
        db_sess.commit()
        return flask.jsonify({'sucsess': 'OK'})

    def get(self):
        db_sess = db_session.create_session()
        librarian = db_sess.query(Librarian).all()
        return flask.jsonify({'librarians': [item.to_dict(only=('surname', 'name', 'middlename', 'email', 'phonenumber', 'hashed_password')) for item in librarian]})
