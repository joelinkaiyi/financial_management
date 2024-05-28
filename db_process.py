from flask import Flask, g
import sqlite3


def getDB():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect('datafile.db')
    return g.sqlite_db


def closeConnection(exception):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .home import bp as home_bp
        app.register_blueprint(home_bp)

    app.teardown_appcontext(closeConnection)

    return app
