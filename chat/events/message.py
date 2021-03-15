from flask_socketio import emit, join_room, leave_room

from chat import socketio
from flask import Blueprint, render_template, request, session, redirect, url_for

bp_chat = Blueprint('message', __name__)


@bp_chat.route('/')
def join():
    return render_template('join.html')


@bp_chat.route('/room', methods=['GET', 'POST'])
def room():
    data = request.json

    session['nick'] = data['nick']
    session['room'] = data['room']
    return "ok"


@bp_chat.route('/chat')
def chat():
    nick = session.get('nick', '')
    room = session.get('room', '')

    if nick == '' or room == '':
        return redirect(url_for('message.join'))

    return render_template('chat.html', nick=nick, room=room)


@socketio.on("message", namespace='/chat')
def handle_message(message):
    room = session.get('room', '')
    emit('message', {'msg': f"{message['nick']}: {message['msg']}"}, namespace='/chat', broadcast=True,
         room=room)  # emitujemy event message do frontendu


@socketio.on("joined", namespace='/chat')
def handle_connect(connect):
    join_room(session['room'])


@socketio.on("left", namespace='/chat')
def handle_leave(connect):
    leave_room(session['room'])
