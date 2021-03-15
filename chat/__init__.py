

from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'

    socketio.init_app(app)

    from chat.views import bp_main
    app.register_blueprint(bp_main, url_prefix='/')

    from chat.events.message import bp_chat
    app.register_blueprint(bp_chat, url_prefix='/chat')

    return app
