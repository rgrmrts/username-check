# Username Check

Script that enumerates all `n` character usernames that are available. Should be general enough to work with github, twitter, and others. A URL scheme needs to be provided and a `404` must be returned if the username does not exist.

# Usage

There's really only one dependency (`requests`) so you don't need to use a virtual environment but I've made it a habit to.

Get your environment set up:

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.lock
```

Modify the number of characters and the website being tested in the script, then run:

```
$ python check.py
```
