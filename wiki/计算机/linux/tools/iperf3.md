

---

# iperf3 网络测试工具



服务端：

```
$ iperf3 -s
```

客户端：

```
$ iperf3 -c <server_addr>
```

默认行为是C向S发数据，客户端使用`-R`参数可以使发送数据的方向反转。



服务端输出例：

```
[r@r-lc sk]$ iperf3 -s
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
Accepted connection from ::1, port 45438
[  5] local ::1 port 5201 connected to ::1 port 45440
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-1.00   sec  4.94 GBytes  42.4 Gbits/sec               
[  5]   1.00-2.00   sec  4.67 GBytes  40.1 Gbits/sec               
[  5]   2.00-3.00   sec  4.67 GBytes  40.1 Gbits/sec               
[  5]   3.00-4.00   sec  4.92 GBytes  42.3 Gbits/sec               
[  5]   4.00-5.00   sec  4.85 GBytes  41.7 Gbits/sec               
[  5]   5.00-6.00   sec  4.98 GBytes  42.8 Gbits/sec               
[  5]   6.00-7.00   sec  4.94 GBytes  42.5 Gbits/sec               
[  5]   7.00-8.00   sec  4.66 GBytes  40.0 Gbits/sec               
[  5]   8.00-9.00   sec  4.85 GBytes  41.6 Gbits/sec               
[  5]   9.00-10.00  sec  4.20 GBytes  36.1 Gbits/sec               
[  5]  10.00-10.00  sec  1.00 MBytes  41.3 Gbits/sec               
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-10.00  sec  47.7 GBytes  41.0 Gbits/sec                  receiver
```

客户端输出例：

```
[r@r-lc wiki]$ iperf3 -c localhost
Connecting to host localhost, port 5201
[  5] local ::1 port 45440 connected to ::1 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  4.94 GBytes  42.4 Gbits/sec    0   1.25 MBytes
[  5]   1.00-2.00   sec  4.67 GBytes  40.1 Gbits/sec    0   1.25 MBytes
[  5]   2.00-3.00   sec  4.67 GBytes  40.1 Gbits/sec    0   1.25 MBytes
[  5]   3.00-4.00   sec  4.92 GBytes  42.3 Gbits/sec    0   1.37 MBytes
[  5]   4.00-5.00   sec  4.85 GBytes  41.7 Gbits/sec    0   1.37 MBytes
[  5]   5.00-6.00   sec  4.98 GBytes  42.8 Gbits/sec    0   1.37 MBytes
[  5]   6.00-7.00   sec  4.94 GBytes  42.5 Gbits/sec    0   1.37 MBytes
[  5]   7.00-8.00   sec  4.66 GBytes  40.0 Gbits/sec    0   1.37 MBytes
[  5]   8.00-9.00   sec  4.85 GBytes  41.6 Gbits/sec    0   1.37 MBytes
[  5]   9.00-10.00  sec  4.20 GBytes  36.1 Gbits/sec    0   1.37 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  47.7 GBytes  41.0 Gbits/sec    0             sender
[  5]   0.00-10.00  sec  47.7 GBytes  41.0 Gbits/sec                  receiver

iperf Done.
```

