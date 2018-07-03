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
    "SLEEP_TIMEOUT": 3,  # in seconds
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


class RedisCache(object):
    def __init__(self, config, log=None):
        if not config:
            raise ValueError("Config is empty")
        self.config = config

        self.log = log if log else get_log()
        self.cache = {}

        self.conn = redis.StrictRedis(
            host=self.config["HOST"],
            port=self.config["PORT"],
            db=self.config["DB"],
            socket_timeout=self.config["SOCKET_TIMEOUT"]
        )

    @staticmethod
    def ensure_connection(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            return method(self, *args, **kwargs)
        return wrapper

    def cache_get(self, key):
        """
        Get value with key firstly from Redis
        but if it fails then from local cache
        """
        value = self.cache.get(key)
        self.log.info("received value: %s from inner cache", value)
        return value

    def cache_set(self, key, value, expired=None):
        self.cache[key] = value
        self.log.info("set key: %s with value: %s to "
                      "inner store", key, value)

    def get(self, key):
        """ Retrive value from Redis """

    def set(self, key, value):
        """ Save value directly to Redis """

