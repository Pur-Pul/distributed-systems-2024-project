import os
import redis
from flask import Flask, jsonify
from flask_cors import CORS
from bitstring import BitArray

app =  Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
redis_cache = redis.Redis()

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
