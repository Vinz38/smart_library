import flask

from data import db_session
from data.books import Book
from flask_restful import reqparse, abort, Api, Resource


def abort_if_book_not_found(book_id):
    session = db_session.create_session()
    books = session.query(Book).get(book_id)
    if not books:
        abort(404, message=f"Book {book_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('namebook', required=True)
parser.add_argument('name_author', required=True)
parser.add_argument('isbn', required=True, type=str)
parser.add_argument('yep', required=True, type=int)
parser.add_argument('taken', required=True, type=bool)
parser.add_argument('tbw', required=False, type=str)


class BookResourse(Resource):
    def put(self, book_id):
        abort_if_book_not_found(book_id)
        args = parser.parse_args()
        db_sess = db_session.create_session()
        book = db_sess.get(Book, book_id)

        book.name_book = args['namebook']
        book.name_author = args['name_author']
        book.isbn = args['isbn']
        book.yep = args['yep']
        book.taken = args['taken']
        book.tbw = args['tbw']

        db_sess.commit()
        return flask.jsonify({'status': 'success'})

    def delete(self, book_id):
        abort_if_book_not_found(book_id)
        db_sess = db_session.create_session()
        book = db_sess.get(Book, book_id)
        db_sess.delete(book)
        db_sess.commit()
        return flask.jsonify({"sucsess": "OK"})


class BookListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        books = db_sess.query(Book).all()
        return [item.to_dict(only=("id", "name_book", "name_author", "isbn", "yep", "taken", "tbw")) for item in books]
    

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
