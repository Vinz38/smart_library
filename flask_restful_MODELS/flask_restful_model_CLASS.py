import flask

from data import db_session
from data.books import Book
from flask_restful import reqparse, abort, Api, Resource

parser = reqparse.RequestParser()
parser.add_argument('class_name', required=True)


class BookListResource(Resource):
    def get(self):
        session = db_session.create_session()
        books = session.query(Book).all()
        return flask.jsonify({"books": [item.to_dict(only=("class_name")) for item in books]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        book = Book(
            name_book=args['class_name'],
        )

        db_sess.add(book)
        db_sess.commit()
        return flask.jsonify({'if': book.id})
