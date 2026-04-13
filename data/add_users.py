import flask

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_add_api',
    __name__,
)

@blueprint.route('/api/add_users', methods=["GET", "POST"])
def get_news():
    db_sess = db_session.create_session()

    users = User(
        surname=flask.request.json['surname'],
        name=flask.request.json['name'],
        middlename=flask.request.json['middlename'],
        email=flask.request.json['email'],
        class_name=flask.request.json['class_name'],
    )

    db_sess.add(users)
    db_sess.commit()

