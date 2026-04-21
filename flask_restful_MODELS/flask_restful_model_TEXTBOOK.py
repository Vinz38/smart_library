import flask

from data import db_session
from data.textbook import TextBook

from flask_restful import reqparse, abort, Api, Resource

parser = reqparse.RequestParser()
parser.add_argument('itemtype', required=True, type=str)
parser.add_argument('tbn', required=True, type=str)
parser.add_argument('yep', required=True, type=int)
parser.add_argument('fwc', required=True, type=str)
parser.add_argument('id_book', required=True, type=int)
parser.add_argument('authors_list', required=True, type=str)
parser.add_argument('taken', required=True, type=bool)
parser.add_argument('tbw', required=False)


def abort_if_news_not_found(textbook_id):
    session = db_session.create_session()
    textbook = session.query(TextBook).get(textbook_id)
    if not textbook:
        abort(404, message=f"Textbook {textbook_id} not found")


class TextBookListResource(Resource):
    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        textbooks = TextBook(
            itemtype=args['itemtype'],
            id_book=args['id_book'],
            tbn=args['tbn'],
            yep=args['yep'],
            fwc=args['fwc'],
            authors_list=args['authors_list'],
            taken=args['taken']
        )

        db_sess.add(textbooks)
        db_sess.commit()

        return flask.jsonify({
            "status": "success"
        }), 200

    def get(self):
        db_sess = db_session.create_session()
        textbook = db_sess.query(TextBook).all()
        return flask.jsonify({"textbooks": [item.to_dict(only=("itemtype", "tbn", "yep", "fwc", "id_book", "authors_list", "taken", "tbw")) for item in textbook]})


class TextBookResource(Resource):
    def put(self, textbook_id):
        abort_if_news_not_found(textbook_id)
        args = parser.parse_args()
        db_sess = db_session.create_session()
        textbook = db_sess.get(TextBook, textbook_id)

        textbook.itemtype = args['itemtype']
        textbook.tbn = args['tbn']
        textbook.yep = args['yep']
        textbook.fwc = args['fwc']
        textbook.id_book = args['id_book']
        textbook.authors_list = args['authors_list']
        textbook.taken = args['taken']
        textbook.tbw = args['tbw']

        db_sess.commit()
        return flask.jsonify({"status": "success"})

    def delete(self, textbook_id):
        abort_if_news_not_found(textbook_id)
        db_sess = db_session.create_session()
        textbook = db_sess.get(TextBook, textbook_id)
        db_sess.delete(textbook)
        db_sess.commit()
        return flask.jsonify({"success": "OK"})
