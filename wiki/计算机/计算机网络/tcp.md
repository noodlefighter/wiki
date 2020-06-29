



## TCP Delayed ACK

收到TCP包应该给ACK，如果收包，那么ACK也会很频繁的发回，所以有了TCP ACK Delay技术，接收方有个定时器，隔一段时间批量发一次ACK（典型10ms）。

## TCP Nagle Algorithm

当tcp协议用来传输小的数据段时代码是很高的,并且如果传输是在广域网上,那可能就会引起网络拥塞.Nagle算法就是用来解决这个问题.该算法要求一个TCP连接上最多只能有一个未被确认(未收到Ack确认)的未完成的小分组，在该分组的确认到达之前不能发送其他的小分组。相反TCP收集这些少量的分组，并在确认到来时以一个分组的方式发出去.Host Requirements RFC声明TCP必须实现Nagle算法，但必须为应用提供一种方法来关闭该算法在某个连接上执行。
纳格算法是合并(coalescing)一定数量的输出资料后一次送出。特别的是，只要有已送出的封包尚未确认，传送者会持续缓冲封包，直到累积一定数量的资料才送出。

via: https://www.cnblogs.com/sunlyk/p/7442474.html



## TCP FIN_WAIT1

```
# netstat
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      1 192.168.8.1:4647        192.168.8.93:49155      FIN_WAIT1
tcp        0      1 192.168.8.1:4647        192.168.8.93:49154      FIN_WAIT1
```

有时候服务端程序已经退出了，但开放的端口还依旧卡在`FIN_WAIT1`这个状态，于是找到了这篇文章：[关于FIN_WAIT1](https://blog.huoding.com/2014/11/06/383)



## TCP Socket options

https://linux.die.net/man/7/tcp