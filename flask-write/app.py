from flask import Flask, jsonify, request
from flask_cors import CORS
from bitstring import BitArray


from flask_socketio import Namespace, emit, SocketIO
import socketio as sock

app =  Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

socketio = SocketIO(app, cors_allowed_origins=['http://localhost:5173', 'http://localhost:5001'])

sio_update = sock.Client()
sio_update.connect('http://localhost:5002/write')

sio_redis = sock.Client()
sio_redis.connect('http://localhost:5000/write')

write_clients = []

@socketio.on('connect', namespace='/write')
def handle_write_connect():
    print('Client connected to write')
    write_clients.append(request.sid)

@socketio.on('disconnect', namespace='/write')
def handle_write_connect():
    print('Client disconnected from write')
    write_clients.remove(request.sid)

@socketio.on('write', namespace='/write')
def handle_write(json):
    print(f'handle write: {json}')
    sio_redis.emit('write', json)

@sio_redis.on('update')
def handle_write_from_redis(json):
    print(f'handle write from redis: {json}')
    sio_update.emit('update', json)