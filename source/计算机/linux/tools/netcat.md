

---

## netcat的两个版本

一般发行版仓库里有两个版本:
* bsd-netcat
* gnu-netcat

gnu这个用的时候得注意这样是不行的, 得用-p参数指定端口
```
nc -l 9898
```
很好, 我选择bsd的实现.



## 用nc测试不断地连接、断开

```
watch -n 0.1 "echo sdfadf |nc -w0 -N localhost 4646"
```



## socat - Multipurpose relay

http://www.dest-unreach.org/socat/
http://www.dest-unreach.org/socat/doc/socat.html

“多用途中继”,看着是想代替netcat.

