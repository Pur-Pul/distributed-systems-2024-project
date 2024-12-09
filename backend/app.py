from flask import Flask, jsonify, request
from flask_cors import CORS
from bitstring import BitArray
from dotenv import load_dotenv
from flask_socketio import Namespace, emit, SocketIO
from urllib.parse import urlparse
import os
import requests
import redis

load_dotenv()
  

redis_url = urlparse(os.environ.get("REDIS_URL"))
flask_index = int(os.getenv("FLASK_INDEX"))
peer_url = os.environ.get("PEER_URL") 
whitelist = os.environ.get("WHITELIST").split(',')

print(whitelist)

redis_cache = redis.Redis(host=redis_url.hostname, port=redis_url.port, username=redis_url.username, password=redis_url.password, ssl=True, ssl_cert_reqs=None)
app =  Flask(__name__)
CORS(app, origins=whitelist)
socketio = SocketIO(app, host='0.0.0.0', port='8000', cors_allowed_origins=whitelist)

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
    if (index > 500_000 and flask_index == 1) or (index < 500_000 and flask_index == 0):
        #peer_url = f"http://localhost:{peer_port}/update/{index}"
        peer_response =requests.post(peer_url+f'/update{index}')
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
    #peer_url = f"http://localhost:{peer_port}/notify"
    data = {'index': index, 'value': value}
    requests.post(peer_url+'/notify', json=data)

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    print('received notify data: ', data)
    index = data['index']
    value = data['value']
    response = {'index': index, 'value': value}
    socketio.emit('update', response)
    return response
