

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

