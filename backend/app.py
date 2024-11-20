import redis
import json as JSON
from flask import Flask, jsonify
from flask_cors import CORS
from bitstring import BitArray


from flask_socketio import Namespace, emit, send, SocketIO

app =  Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
redis_cache = redis.Redis()
socketio = SocketIO(app, cors_allowed_origins=['http://localhost:5173'])

@app.route("/", methods=['GET'])
def index():
    response = jsonify({'state' : BitArray(redis_cache.get('state')).bin})
    return response

@app.route("/update/<int:index>", methods=['POST'])
def update(index):
    value = redis_cache.getbit('state', index)
    value = (value+1) % 2
    redis_cache.setbit('state', index, value)
    response = jsonify({'index' : index, 'value' : value})
    return response


@socketio.on('state', namespace='/state')
def handle_state(json):
    print('received json: ' + str(json))
    chunk_index = json['data']
    response = BitArray(redis_cache.get(chunk_index)).bin
    emit('state', response)

@socketio.on('write', namespace='/write')
def handle_write(json):
    print('received json: ' + str(json))
    index = int(json['data'])
    value = redis_cache.getbit('state', index)
    value = (value + 1) % 2
    redis_cache.setbit('state', index, value)
    response = {'index' : index, 'value' : value}
    emit('update', response)
