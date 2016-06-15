import os
from threading import Thread

import bottle
import redis


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


class Publisher:
    """
    In charge of publishing messages to Redis
    """

    """
    The channel the publisher sends data to
    """
    Channel = 'test'

    def __init__(self, redis):
        self._redis = redis

    def publish(self):
        """
        Publish the json parsable content of the request to the Redis channel and return it
        """
        from bottle import request
        json = request.json
        self._redis.publish(self.Channel, json)
        return json

    def run(self):
        """
        Run the webserver (blocking)
        """
        bottle.post('/publish')(self.publish)
        bottle.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    r = redis_from_env()

    publisher = Publisher(r)

    pubsub = r.pubsub()
    pubsub.subscribe(publisher.Channel)
    thread = Thread(target=listen, args=(pubsub,))
    thread.start()

    publisher.run()
