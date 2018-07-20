
# Unit and integration tests for scoring API
It's extended set or tests for Scoring API.
It includes:
- tests for fields in file: `test_fields.py`
- tests for store in file: `test_store.py`
- integration test for API in file: `test_integration.py`

*Before running integration tests the API in `api.py` and `redis-server` should be up and running on your machine*

## How to run
It developed and tested on Python *2.7.12*. So this version should be installed in your system.
```
$ git clone https://github.com/ligain/04_testing
$ cd 04_testing
$ virtualenv -p /usr/bin/python2.7 .env
$ source .env/bin/activate
$ pip install -r requirements.txt
$ python api.py
[2018.07.07 14:57:31] I Starting server at 8080
$ python -m pytest tests/
```
Output should looks like:
```
$ python -m pytest tests/
================================================ test session starts ================================================
platform linux2 -- Python 2.7.12, pytest-3.6.2, py-1.5.4, pluggy-0.6.0
rootdir: /home/linder/PycharmProjects/otus-python/04_testing, inifile:
collected 81 items

tests/test_fields.py .................................................                                        [ 60%]
tests/test_integration.py ............................                                                        [ 95%]
tests/test_store.py ....                                                                                      [100%]

============================================ 81 passed in 51.91 seconds =============================================
```
### Project Goals
The code is written for educational purposes.
