'''
В этом файле пишем QT дизайн и привязываем все к нопкам и т.д.
'''
from data import db_session, add_book, add_textbook, add_users, register_lib
from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)

api.add_resource(add_book.BookResourse, '/api/add_book')


@app.route('/main')
def main():
    return "OK"


if __name__ == "__main__":
    db_session.global_init('db/library.db')
    app.run(port=8080, host='127.0.0.1')
