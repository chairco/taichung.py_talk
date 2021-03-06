# taichung.py.talk 分享


## 20181013 搞懂 Python 協同程序(Coroutine): 快樂學會非同步程式開發 

[投影片](https://slides.com/chairco/how_coroutine_work_in_python/#/)


### 摘要

單一執行緒(single thread)底下允許程式來決定程式執行的順序，是基於`協同程序(Coroutine)`來實現非同步的其中一種策略。因為 Python(`CPython`) 的 `GIL(Global Interpreter Lock)` 特性，這個方法提供了解決**某些**類型`非同步`問題。

Python 基本上是以`同步`程式開發精神為設計，因此 Python `非同步`開發與`同步`開發是兩種不同的思維與世界。本次將會分享 Python 使用`協同程序`開發非同步與其概念，並且如何手寫一個`協同程序`，接續介紹 3.5 版後的 `asyc` 與 `await` 語法所創造的`協同程序`。

分享的最後會以一個 Serial port 範例來 Demo 如何快快樂樂實現 Python 非同步程式開發。


### 大綱

+ 非同步的策略介紹
+ 非阻塞式事件驅動與 Coroutine 的非同步策略
+ 協同程序(Coroutine)是什麼？可以吃嗎？（透過一個同步且阻塞式的 Socket 來連接網頁做範例程式說明）
    - Non-blocking I/O
    - Callback
    - Event loop
    - Coroutine
+ 登愣！async, await 登場
    - async 語法所創造協同程序
    - async 語法所創造產生器
    - 怎麼使用 asyncio 的 event loop 來建立事件迴圈並開發非同步程式
+ Demo 
    - serial port


### 講者簡介

喜愛使用 Python 開發軟體，目前是一位資料與數據分析工程師。喜歡貓貓與狗狗，因此假日的嗜好就是帶著另一半去餵食浪浪們。

more: https://chairco.github.io


### 文章參考

+ [Python asyncio cheatsheet](https://www.pythonsheets.com/notes/python-asyncio.html)
+ [async def v.s @asyncio.coroutine](https://stackoverflow.com/questions/40571786/asyncio-coroutine-vs-async-def)
