import flask

from . import db_session
from .librarians import Librarian

blueprint = flask.Blueprint(
    'register_lib_api',
    __name__,
)


@blueprint.route('/api/reg_lib', methods=["GET", "POST"])
def get_news():
    db_sess = db_session.create_session()

    librarian = Librarian(
        surname=flask.request.json['surname'],
        name=flask.request.json['name'],
        middlename=flask.request.json['middlename'],
        email=flask.request.json['email'],
        class_name=flask.request.json['phonenumber'],
    )
    librarian.set_password(flask.request.json['hashed_password'])
    db_sess.add(librarian)
    db_sess.commit()
