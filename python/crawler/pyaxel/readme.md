Pyaxel
---

Pyaxel is a lightweight command line download accelerator for Linux and MacOS wrote with python Inspired by [axel](https://github.com/eribertomota/axel).

Features
---

* Support HTTP, HTTPS protocols
* Support multi thread and coroutine
* Easy to use


Installation
---

Just support python3 right now

```python
pip3 install -r requirements.txt
```

Usage
---

```python
python3 axel.py [URL]
```

or put `axel.py` into your $PATH, and rename to axel, then

```python
axel [URL]
```

TODO
---

* Complete supporting `gevent` and `asyncio`
* Progress bar
* Breakpoint resume


Getting help
---

Just open an [issue]()