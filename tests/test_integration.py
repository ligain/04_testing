import hashlib

import datetime
import pytest
import requests

import api

API_URL = "http://127.0.0.1:8080/method"


@pytest.fixture
def api_request():
    def _make_api_request(data=None):
        return requests.post(
            API_URL,
            json=data
        )
    return _make_api_request


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
    assert resp.status_code == api.FORBIDDEN


@pytest.mark.parametrize("data", [
    {"account": "test_acc", "login": "test_login", "method": "online_score", "token": "", "arguments": {}},
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
    if data["login"] == api.ADMIN_LOGIN:
        data["token"] = hashlib.sha512(datetime.datetime.now().strftime("%Y%m%d%H") + api.ADMIN_SALT).hexdigest()
    else:
        data["token"] = hashlib.sha512(data.get("account") + data.get("login") + api.SALT).hexdigest()
    resp = api_request(data)
    assert resp.status_code == api.INVALID_REQUEST


@pytest.mark.parametrize("data", [
    {"account": "test_acc", "login": "test_login", "method": "clients_interests", "token": "", "arguments": {}},
])
def test_clients_interests(data, api_request):
    pass
