import redis
from flask import Flask, jsonify, request
from flask_cors import CORS
from bitstring import BitArray
import os
import requests


from flask_socketio import Namespace, emit, SocketIO

app =  Flask(__name__)
current_port = int(os.getenv("FLASK_RUN_PORT"))
peer_port = 5000 if current_port == 5001 else 5001 
CORS(app, origins=["http://localhost:5000", "http://localhost:5001", "http://localhost:5173"])
redis_cache = redis.Redis()
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5001", "http://localhost:5002", "http://localhost:5173"])

@app.route("/", methods=['GET'])
def index():
    response = jsonify({'state' : BitArray(redis_cache.get('state')).bin})
    return response

@app.route("/update/<int:index>", methods=['POST'])
def update(index):
    value = redis_cache.getbit('state', index)
    value = (value+1) % 2
    redis_cache.setbit('state', index, value)
    response = {'index': index, 'value': value}
    socketio.emit('update', response)
    return jsonify(response)

@socketio.on('connect')
def handle_state_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_state_connect():
    print('Client disconnected')

@socketio.on('state')
def handle_state(json):
    print('received json: ' + str(json))
    chunk_index = json['data']
    response = BitArray(redis_cache.get(chunk_index)).bin
    emit('state', response)

@socketio.on('write')
def handle_write(json):
    print('received json: ' + str(json))
    index = int(json['data'])
    if (index > 500_000 and current_port == 5000) or (index < 500_000 and current_port == 5001):
        peer_url = f"http://localhost:{peer_port}/update/{index}"
        peer_response =requests.post(peer_url)
        if peer_response.status_code == 200:
            response_data = peer_response.json()
            emit('update', response_data, broadcast=True)
        return
    value = redis_cache.getbit('state', index)
    value = (value + 1) % 2
    redis_cache.setbit('state', index, value)
    response = {'index' : index, 'value' : value}
    emit('update', response, broadcast = True)
    notify_peer(index, value)

def notify_peer(index, value):
    peer_url = f"http://localhost:{peer_port}/notify"
    data = {'index': index, 'value': value}
    requests.post(peer_url, json=data)

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    print('received notify data: ', data)
    index = data['index']
    value = data['value']
    response = {'index': index, 'value': value}
    socketio.emit('update', response)
    return response
