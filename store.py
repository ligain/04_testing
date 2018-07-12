import redis
import logging
import time

from functools import wraps

# Example of Redis config
REDIS_CONFIG = {
    "HOST": "localhost",
    "PORT": 6379,
    "DB": 0,
    "ATTEMPTS": 5,
    "SLEEP_TIMEOUT": 3,   # in seconds
    "SOCKET_TIMEOUT": 5,
}


def get_log():
    logging.basicConfig(
        format="[%(asctime)s] %(levelname).1s %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    return logger


def ensure_connection(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.conn is None:
            attempts = self.config["ATTEMPTS"]
            while True:
                self.conn = redis.StrictRedis(
                    host=self.config["HOST"],
                    port=self.config["PORT"],
                    db=self.config["DB"],
                    socket_timeout=self.config["SOCKET_TIMEOUT"]
                )
                try:
                    self.conn.ping()
                    break
                except redis.ConnectionError, redis.TimeoutError:
                    time.sleep(self.config["SLEEP_TIMEOUT"])
                if attempts == -1 or attempts is None:
                    continue
                elif isinstance(attempts, int) and attempts > 0:
                    attempts -= 1
                else:
                    break
        return method(self, *args, **kwargs)
    return wrapper


class RedisCache(object):
    def __init__(self, config, log=None):
        if not config:
            raise ValueError("Config is empty")
        self.config = config

        self.log = log if log else get_log()
        self.cache = {}
        self.conn = None

    def connect(self):
        self.conn = redis.StrictRedis(
            host=self.config["HOST"],
            port=self.config["PORT"],
            db=self.config["DB"],
            socket_timeout=self.config["SOCKET_TIMEOUT"]
        )
        return self

    @ensure_connection
    def cache_get(self, key):
        """
        Get value with key firstly from Redis
        but if it fails then from local cache
        """
        try:
            value = self.conn.get(key)
        except redis.ConnectionError:
            self.log.error("Redis is down. Please reload Redis sever")
            value = None

        if value is None:
            self.log.info("there is no such key: %s in Redis", key)
            value = self.cache.get(key)
        return value

    @ensure_connection
    def cache_set(self, key, value, expired=None):
        self.cache[key] = str(value)
        self.log.info("set key: %s with value: %s to "
                      "inner store", key, value)
        try:
            self.conn.set(key, value, ex=expired)
        except redis.ConnectionError:
            self.log.error("Error on setting key: %s with value: %s. "
                           "Redis is down.", key, value)

    @ensure_connection
    def get(self, key):
        """ Retrive value from Redis """
        self.log.info("receiving value by key: %s from Redis", key)
        return self.conn.get(key)

    @ensure_connection
    def set(self, key, value):
        """ Save value directly to Redis """
        self.log.info("saving value: %s with key: %s to Redis", value, key)
        self.conn.set(key, value)

    @ensure_connection
    def delete(self, key):
        """ Delete key directly from Redis """
        self.log.info("delete key: %s from Redis", key)
        self.conn.delete(key)
