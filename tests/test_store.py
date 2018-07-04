import pytest
import uuid

from store import RedisCache, REDIS_CONFIG


@pytest.fixture
def redis_store(config=REDIS_CONFIG):
    return RedisCache(config=config)


def test_store_connection(redis_store):
    assert redis_store.conn.ping(), "Redis is down"


def test_read_wrong_key_from_store(redis_store):
    wrong_key = str(uuid.uuid4())
    assert redis_store.cache_get(wrong_key) is None
    assert redis_store.get(wrong_key) is None