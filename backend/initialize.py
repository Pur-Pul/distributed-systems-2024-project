import redis
from bitstring import BitArray

redis_cache = redis.Redis()

s = BitArray(length=1000000)
redis_cache.set('state', s.tobytes())
print(redis_cache.memory_usage('state'))


