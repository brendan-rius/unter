import redis

r = redis.Redis('redis')
r.set('foo', 'bar')
value = r.get('foo')
print(value)
