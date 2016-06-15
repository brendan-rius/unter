import os
from threading import Thread

import redis
import time


def redis_from_env():
    """
    Create a connection to Redis from the environment variables
    :return:
    """
    try:
        host = os.environ['REDIS_HOST']
    except KeyError:
        raise Exception('Please specify Redis host in env variable "REDIS_HOST"')
    try:
        db = os.environ['REDIS_DB']
    except KeyError:
        raise Exception('Please specify Redis database in env variable "REDIS_DB"')
    try:
        port = os.environ['REDIS_PORT']
    except KeyError:
        raise Exception('Please specify Redis port in env variable "REDIS_PORT"')

    config = {
        'host': host,
        'port': port,
        'db': db,
    }

    return redis.StrictRedis(**config)


def listen(pubsub):
    """
    Listen to a pubsub object and writes the received data.
    This is blocking.
    :param pubsub: the Redis pubsub object
    """
    while True:
        for item in pubsub.listen():
            print('Received: {}'.format(item['data']))


if __name__ == '__main__':
    r = redis_from_env()
    pubsub = r.pubsub()
    pubsub.subscribe('test')
    print('Listening to channel')

    thread = Thread(target=listen, args=(pubsub,))
    thread.start()
    for i in range(10):
        print("Publish")
        r.publish('test', i)
        time.sleep(1)
