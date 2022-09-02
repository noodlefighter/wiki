## python使用utf编码

```
#!/usr/bin/python
# -*- coding: UTF-8 -*-
```

## Python2

让python2的print兼容python3，即是一个函数

```
from __future__ import print_function
```



## Python装饰器

```
def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
```

实例，要求执行`do_something()`先检查是否已连接：

```
import asyncio
import websockets

class WsUbus:
    def __init__(self):
        self.connected = False

    def need_connected(func):
        def wrapper(*args, **kw):
            self = args[0]
            if not self.connected:
                raise Exception('not connected, please call connect() first')
            return func(*args, **kw)
        return wrapper

    async def connect(self, uri, username, password):
        if self.connected:
            self.ws.close()

        # connect websocket
        self.ws = await websockets.connect(uri, subprotocols=['ubus-json'])
        self.connected = True

    @need_connected
    async def do_something(self):
        print('do_something')

async def test():
    wu = WsUbus()
    # 屏蔽这句
    # await wu.connect(WS_UBUS_URI, 'api', 'api')
    await wu.do_something()

asyncio.get_event_loop().run_until_complete(test())

```

## python全局变量global关键字

```
a = 3
def Fuc():
	global a
    print (a)
    a=a+1
Fuc()
```

## python保存requirements.txt

```
pip freeze > requirements.txt
```

## python添加模块搜索路径

```
import os
import sys
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../simplecborrpc')
```

## python独立执行模块时测试

```
if __name__ == '__main__':
    # do some test
```



## python保存二进制文件



```
with open('name.jpg', 'wb') as file:
    file.write(b'1001001')
```



## python regex 正则

```
#!/usr/bin/env python
#encoding: utf-8
import re
url = 'https://113.215.20.136:9011/113.215.6.77/c3pr90ntcya0/youku/6981496DC9913B8321BFE4A4E73/0300010E0C51F10D86F80703BAF2B1ADC67C80-E0F6-4FF8-B570-7DC5603F9F40.flv'
pattern = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
print pattern.findall(url)
out = re.sub(pattern, '127.0.0.1', url)
print out
```





## python的asyncio



### 并行运行两个async函数

```

async def thread1():
	while True:
		print('thread1')
		await asyncio.sleep(1)
	
async def thread1():
	while True:
		print('thread2')
		await asyncio.sleep(2)
	
asyncio.get_event_loop().run_until_complete(asyncio.gather(thread1(), thread2()))
```



### python的asyncio异步队列

> via: https://cloud.tencent.com/developer/article/1638916

```
import asyncio
import random
import aiohttp


async def producer(queue):
    for i in range(10):
        await queue.put(i)
        await asyncio.sleep(random.randint(1, 3))


async def consumer(queue):
    while True:
        sleep_time = await queue.get()
        size = queue.qsize()
        print(f'当前队列有：{size} 个元素')
        url = 'http://httpbin.org/delay/2'
        async with aiohttp.ClientSession() as client:
            resp = await client.get(url)
            print(await resp.json())

async def main():
    queue = asyncio.Queue(maxsize=3)
    asyncio.create_task(producer(queue))
    con = asyncio.create_task(consumer(queue))
    await con


asyncio.run(main())
```



## python串口库

库[pyserial](https://pyserial.readthedocs.io/en/latest/shortintro.html)：

```
import serial
import time

bandrate = 921600
s_tx = serial.Serial('/dev/ttyUSB0', bandrate, timeout=0)
s_rx = serial.Serial('/dev/ttyUSB1', bandrate, timeout=0)

data = '1234567890abcdefg'.encode("ascii")
s_tx.write(data)
time.sleep(0.2)
assert(s_rx.readall() == data)

```



## python的函数式编程

Python函数式编程指引:

https://docs.python.org/zh-cn/3/howto/functional.html



filter()、map()、[`enumerate`](https://docs.python.org/zh-cn/3/library/functions.html#enumerate)

## python的lambda

```
list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
[1, 4, 9, 16, 25, 36, 49, 64, 81]


```



## python把当前目录加入模块搜索路径

```
import os, sys
sys.path.append(os.path.curdir)
```



## python脚本中动态执行脚本

python像js一样也有eval函数：

```
def abc():
	print("hahah")
	
eval("abc()")
```

