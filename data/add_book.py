import flask

from . import db_session
from .books import Book
from flask_restful import reqparse, abort, Api, Resource


'''def abort_if_book_not_found(book_id):
    session = db_session.create_session()
    news = session.query(Book).get(book_id)
    if not news:
        abort(404, message=f"Book {book_id} not found")'''


parser = reqparse.RequestParser()
parser.add_argument('namebook', required=True)
parser.add_argument('name_author', required=True)
parser.add_argument('isbn', required=True, type=str)
parser.add_argument('yep', required=True, type=int)
parser.add_argument('taken', required=True, type=bool)


class BookResourse(Resource):
    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        book = Book(
            name_book=args['namebook'],
            name_author=args['name_author'],
            isbn=args['isbn'],
            yep=args['yep'],
            taken=args['taken']
        )

        db_sess.add(book)
        db_sess.commit()
        return flask.jsonify({'if': book.id})
    
    def get(self):
        session = db_session.create_session()
        books = session.query(Book).all()
        return flask.jsonify({'book': [item.to_dict(only=('name_book', 'name_author', 'isbn', 'yep', 'taken')) for item in books]})
