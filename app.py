import os
import redis
from flask import Flask
from bitstring import BitArray

app =  Flask(__name__)
redis_cache = redis.Redis()

@app.route("/")
def index():
    s = BitArray(length=1000000)
    redis_cache.set('state', s.tobytes())
    print(redis_cache.memory_usage('state'))
    return "Hello World!"

@app.route("/update/<int:index>")
def update(index):
    redis_cache.setbit('state', index, 1)
    return "set"

@app.route("/get_state/")
def get_state():
    res = BitArray(redis_cache.get('state'))
    print(res)
    return res.bin