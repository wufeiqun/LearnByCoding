# alexaTop500
Screwling the top 500 websites of the http://www.alexa.com/topsites/global;0 ,just for learning [gevent](https://github.com/gevent/gevent)~

####Introduction

---

&emsp;Before 10.1 holidays,I attend Alibaba's Interview through  telephone,one of the asked questions is about `gevent`, and I was not used it in my work at all,so I learn it the whole holidays.This is a small python script to compare gevent with multiprocessing and multithreading.Any better ideas,just give me an issue,thanks.

####Usage

---

Just clone it and run:

```
pip install requirements.txt
python alexa.py
```

####ScreenShots

---

```

******************************common******************************
Total domains: 500
Total used 10.90 seconds.
******************************multithreading******************************
Total domains: 500
Total used 1.42 seconds.
******************************gevent******************************
Total domains: 500
Total used 1.32 seconds.

```
