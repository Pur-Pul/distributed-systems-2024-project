from flask import Flask, jsonify, request
from flask_cors import CORS
from bitstring import BitArray


from flask_socketio import Namespace, emit, SocketIO
import socketio as sock


app =  Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

socketio = SocketIO(app, cors_allowed_origins=['http://localhost:5173', 'http://localhost:5002' ])

sio_redis = sock.Client()
sio_redis.connect('http://localhost:5000/state')

update_clients = []

@socketio.on('connect', namespace='/state')
def handle_state_connect():
    print(f'Client connected to state: {request.sid}')
    update_clients.append(request.sid)

@socketio.on('disconnect', namespace='/state')
def handle_state_connect():
    print('Client disconnected from state')
    update_clients.remove(request.sid)

@socketio.on('state', namespace='/state')
def handle_state(json):
    print(f'handle state')
    sio_redis.emit('state', json)

@socketio.on('update')#, namespace='/write')
def handle_write(json):
    print(f'handl write: {json}')
    socketio.emit('update', json, namespace='/state')

@sio_redis.on('state')
def handle_state_from_redis(state):
    print("handle state from redis")
    socketio.emit('state', state, namespace='/state')