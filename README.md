# 35_diff_service

This project is designed to show the difference between two text documents, like `git diff`.

[Open app](https://floating-earth-32904.herokuapp.com)

# How it works

At the input two texts - the first is considered the source, the second is changed. Next, the application calculates what has been changed and shown:

* red - deleted blocks
* yellow - moved blocks
* green - inserted blocks

# How to run project on local

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
$ pip install -r requirements.txt # alternatively try pip3
```
Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

Next, run tests:

```bash
$ python -m unittest tests/test.py
```

If all tests will not failed, run application:

```bash
$ python server.py
```

Project will running on http://0.0.0.0:8080/ (see config below to change it)

# Configuration app

The application configuration is in the file `config.py`. It contains:

* `SITE_IP_ADDRESS` - application IP address
* `SITE_PORT` - application port
* `DEBUG` - flask debug mode (1/0)
* `DIFF_CONFIG` - config diff module

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
