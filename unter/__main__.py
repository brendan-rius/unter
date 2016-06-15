import json
import os
import pprint

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


class Dispatcher:
    """
    In charge of publishing messages to Redis
    """

    """
    The channel that gets populated with clients' requests
    """
    RequestsChannel = 'clients'
    ProvidersChannel = 'providers'

    def __init__(self, redis):
        self._redis = redis
        self._pubsub = self._redis.pubsub()
        self._pubsub.subscribe(self.Channel)

    def post(self):
        """
        Publish the json parsable content of the request to the Redis channel and return it
        """
        from bottle import request
        data = request.json
        self._redis.publish(self.Channel, json.dumps(data))
        return data

    def get(self):
        messages = []
        while True:
            message = self._pubsub.get_message()
            if message is None:
                break
            else:
                pprint.pprint(message)
                print(message['data'])
                messages.append(json.loads(message['data'].decode('utf-8')))

        return {'messages': messages}

    def run(self):
        """
        Run the webserver (blocking)
        """
        bottle.post('/data')(self.post)
        bottle.get('/data')(self.get)
        bottle.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    r = redis_from_env()

    publisher = Dispatcher(r)
    publisher.run()
