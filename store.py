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

        for _ in range(self.config["ATTEMPTS"]):
            self.conn = redis.StrictRedis(
                host=self.config["HOST"],
                port=self.config["PORT"],
                db=self.config["DB"],
                socket_timeout=self.config["SOCKET_TIMEOUT"]
            )
            try:
                self.conn.ping()
                break
            except redis.ConnectionError:
                time.sleep(self.config["SLEEP_TIMEOUT"])

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

    def cache_set(self, key, value, expired=None):
        self.cache[key] = value
        self.log.info("set key: %s with value: %s to "
                      "inner store", key, value)
        try:
            self.conn.set(key, value, ex=expired)
        except redis.ConnectionError:
            self.log.error("Error on setting key: %s with value: %s. "
                           "Redis is down.", key, value)

    def get(self, key):
        """ Retrive value from Redis """
        self.log.info("receiving value by key: %s from Redis", key)
        return self.conn.get(key)

    def set(self, key, value):
        """ Save value directly to Redis """
        self.log.info("saving value: %s with key: %s to Redis", value, key)
        self.conn.set(key, value)

