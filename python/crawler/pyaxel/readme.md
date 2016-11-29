Pyaxel
---

Pyaxel is a lightweight command line download accelerator for Linux and MacOS wrote with python Inspired by [axel](https://github.com/eribertomota/axel).

Features
---

* Support HTTP, HTTPS protocols
* Support multi thread and coroutine(todo)
* MD5 checksum
* Show time consumption


Installation
---

Just support python3 right now

```python
pip3 install -r requirements.txt
```

Usage
---

```python
python3 pyaxel.py [URL]
```

or put `pyaxel.py` into your $PATH, and rename to axel, then

```python
axel [URL]
```

more:

```
python pyaxel.py --help
```

ScreenShot
---
![basic](https://raw.githubusercontent.com/hellorocky/blog/master/picture/10.pyaxel.png)


TODO
---

* Complete supporting `gevent` and `asyncio`
* Progress bar
* Breakpoint resume
* Ctrl+C signal handler


Getting help
---

Just open an [issue](https://github.com/hellorocky/LearnByCoding/issues)

Contributions
---

Thanks for some useful suggestion.

https://www.v2ex.com/t/323771