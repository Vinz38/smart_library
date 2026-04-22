import flask

from data import db_session
from data.classes import Class
from flask_restful import reqparse, abort, Api, Resource

parser = reqparse.RequestParser()
parser.add_argument('class_name', required=True, type=str)


class ClassResource(Resource):
    def get(self):
        session = db_session.create_session()
        classes = session.query(Class).all()
        return [item.to_dict(only=("class_name", )) for item in classes]

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        classes = Class(
            class_name=args['class_name']
        )

        db_sess.add(classes)
        db_sess.commit()
        return flask.jsonify({'sucsess': 'OK'})
    

