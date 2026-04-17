import flask

from . import db_session
from .textbook import TextBook

blueprint = flask.Blueprint(
    'textbooks_add_api',
    __name__,
)


@blueprint.route('/api/add_textbook', methods=["POST"])
def get_textbook():
    db_sess = db_session.create_session()

    data = flask.request.get_json()

    if not data:
        return flask.jsonify({"error": "No JSON data provided"}), 400

    required_fields = ["itemtype", "tbn", "yep", "id_book", "authors_list"]
    for field in required_fields:
        if field not in data:
            return flask.jsonify({"error": f"Missing field: {field}"}), 400

    textbooks = TextBook(
        itemtype=data['itemtype'],
        tbn=data['tbn'],
        yep=data['yep'],
        id_book=data['id_book'],
        authors_list=data['authors_list']
    )

    db_sess.add(textbooks)
    db_sess.commit()

    return flask.jsonify({
        "status": "success",
        "message": "Textbook added successfully"
    }), 200