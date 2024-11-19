import os
import redis
from flask import Flask
from bitstring import BitArray

app =  Flask(__name__)
redis_cache = redis.Redis()

@app.route("/")
def index():
    res = BitArray(redis_cache.get('state'))
    print(res)
    return res.bin

@app.route("/update/<int:index>")
def update(index):
    value = redis_cache.getbit('state', index)
    value = (value+1) % 2
    redis_cache.setbit('state', index, value)
    return "set"
