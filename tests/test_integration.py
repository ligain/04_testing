import hashlib
import datetime
import pytest
import requests
import json

from types import DictType
from contextlib import contextmanager

import api
import redis
from store import REDIS_CONFIG
from test_store import redis_bad_store

API_URL = "http://127.0.0.1:8080/method"


def authorize_request(data):
    if isinstance(data, DictType):
        if data.get("login") == api.ADMIN_LOGIN:
            data["token"] = hashlib.sha512(datetime.datetime.now().strftime("%Y%m%d%H") + api.ADMIN_SALT).hexdigest()
        else:
            data["token"] = hashlib.sha512(data.get("account") + data.get("login") + api.SALT).hexdigest()
    return data


@pytest.fixture
def api_request():
    def _make_api_request(data=None):
        return requests.post(
            API_URL,
            json=data
        )
    return _make_api_request


@contextmanager
def redis_set_data(data):
    if not isinstance(data, DictType):
        return
    redis_store = redis.StrictRedis(
        host=REDIS_CONFIG["HOST"],
        port=REDIS_CONFIG["PORT"],
        db=REDIS_CONFIG["DB"]
    )
    try:
        for key, value in data.items():
            redis_store.set(key, value)
        yield redis_store
    finally:
        redis_store.delete(*data.keys())


@pytest.mark.xpass
def test_api_availability(api_request):
    api_request()


@pytest.mark.parametrize("data", [
    {"account": "", "login": "", "method": "online_score", "token": "", "arguments": {}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments": {}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"phone": "71234567890", "email": "test@example.com", "gender": 1, "birthday": "01.01.2000"}}
])
def test_unauthorized_request(data, api_request):
    resp = api_request(data)
    assert api.FORBIDDEN == resp.status_code


@pytest.mark.parametrize("data", [
    {"account": "test_acc", "login": "admin", "method": "online_score", "token": "", "arguments": {}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"phone": "", "email": "", "first_name": "", "last_name": "", "birthday": "", "gender": None}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"phone": None, "email": None}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"phone": "71234567890", "email": None}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"phone": None, "email": None}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"phone": None, "email": "test@example.com"}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"first_name": None, "last_name": None}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"first_name": "", "last_name": ""}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"first_name": "John", "last_name": None}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"first_name": None, "last_name": "Doe"}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"gender": None, "birthday": "01.01.2000"}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"gender": None, "birthday": ""}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"gender": 0, "birthday": None}},
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"gender": None, "birthday": None}},
])
def test_invalid_arguments_pairs(data, api_request):
    authorize_request(data)
    resp = api_request(data)
    assert api.INVALID_REQUEST == resp.status_code


@pytest.mark.parametrize("data, expected", [
    ({"account": "test_acc", "login": "test_login", "method": "clients_interests", "token": "", "arguments":
        {"client_ids": [1, 2, 3], "date": "06.07.2018"}}, {u'1': [], u'2': [], u'3': []}),
    ({"account": "test_acc", "login": "test_login", "method": "clients_interests", "token": "", "arguments":
        {"client_ids": [3], "date": "06.07.2018"}}, {u'3': []}),
])
def test_clients_interests(data, expected, api_request):
    authorize_request(data)
    resp = api_request(data).json()
    assert api.OK == resp.get("code")
    assert expected == resp.get("response")


@pytest.mark.parametrize("data, expected", [
    ({"account": "test_acc", "login": "test_login", "method": "clients_interests", "token": "", "arguments":
        {"client_ids": [1], "date": "06.07.2018"}}, {"1": ["books", "hi-tech"]}),
    ({"account": "test_acc", "login": "test_login", "method": "clients_interests", "token": "", "arguments":
        {"client_ids": [2, 1], "date": "06.07.2018"}}, {"1": ["books", "hi-tech"], "2": ["pets", "tv"]}),
])
def test_clients_interests_value_from_store(data, expected, api_request):
    authorize_request(data)

    result_dict = {"i:%s" % k: json.dumps(v) for k, v in expected.items()}
    with redis_set_data(result_dict):
        resp = api_request(data).json()
        assert expected == resp.get("response")


@pytest.mark.parametrize("data, expected", [
    ({"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"phone": "71234567890", "email": "john@example.com", "first_name": "John", "last_name": "Doe",
         "birthday": "01.01.1990", "gender": 1}}, {"score": "5.0"}),
    ({"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"phone": "71234567890", "email": "john@example.com"}}, {"score": "3.0"}),
    ({"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"first_name": "John", "last_name": "Doe"}}, {"score": "0.5"}),
    ({"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"birthday": "01.01.1990", "gender": 1}}, {"score": "1.5"}),
])
def test_online_score(data, expected, api_request):
    authorize_request(data)
    resp = api_request(data).json()
    assert api.OK == resp.get("code")
    assert expected == resp.get("response")


@pytest.mark.parametrize("data, expected", [
    ({"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"phone": "71234567890", "email": "john@example.com", "first_name": "John", "last_name": "Doe",
         "birthday": "01.01.1990", "gender": 1}}, {"score": "5.0"}),
    ({"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments":
        {"phone": "71234567890", "email": "john@example.com"}}, {"score": "3.0"}),
])
def test_online_score_broken_redis(data, expected, api_request, monkeypatch):
    authorize_request(data)
    with monkeypatch.context() as m:
        m.setattr("store.RedisCache", redis_bad_store())
        resp = api_request(data).json()
        assert api.OK == resp.get("code")
        assert expected == resp.get("response")
