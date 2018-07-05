import pytest
import uuid

import redis
import time

from store import RedisCache, REDIS_CONFIG

REDIS_BAD_CONFIG = {
    "HOST": "wrong_host",
    "PORT": 6379,
    "DB": 0,
    "ATTEMPTS": 5,
    "SLEEP_TIMEOUT": 3,   # in seconds
    "SOCKET_TIMEOUT": 5,  # in seconds
}


@pytest.fixture
def redis_store(config=REDIS_CONFIG):
    return RedisCache(config=config)


@pytest.fixture
def redis_bad_store(config=REDIS_BAD_CONFIG):
    return RedisCache(config=config)


def test_store_connection(redis_store):
    assert redis_store.conn.ping(), "Redis is down"


def test_read_wrong_key_from_store(redis_store):
    wrong_key = str(uuid.uuid4())
    assert redis_store.cache_get(wrong_key) is None
    assert redis_store.get(wrong_key) is None


def test_cache_store_with_wrong_redis_conn(redis_bad_store):
    redis_bad_store.cache_set("test_key", 42)
    assert redis_bad_store.cache_get("test_key") == 42
    with pytest.raises(redis.ConnectionError):
        redis_bad_store.set("test_key", 42)
        redis_bad_store.get("test_key")


def test_save_value_with_expiration(redis_store):
    redis_store.cache_set("test_key_with_expiration", 42, 1)
    redis_store.set("test_key_with_expiration2", 42)
    redis_store.cache_set("test_key_with_expiration3", [1, 2, 3], 1)
    time.sleep(3)
    assert redis_store.cache_get("test_key_with_expiration") == 42
    assert redis_store.get("test_key_with_expiration2") == str(42)
    assert redis_store.get("test_key_with_expiration3") is None
