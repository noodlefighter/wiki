---



## 代理工具

proxychanins 走代理的工具
nc 瑞士军刀netcat
squid 正向、反向代理，web缓存



## 让chrome走代理

```
/usr/bin/google-chrome-stable --http-proxy=xxxx.net:8080 --https-proxy=xxxxx.net:8080 %U
```

## Linux设置代理（http）

> via: <https://www.cnblogs.com/EasonJim/p/9826681.html>

我谈一下这个http_proxy的设置，首先，设置了这个变量不是说只会走http协议，上面我说的应该是普通认为会这样说的说法，我后面觉得上面已经是错误了，比如curl，git这些软件默认使用http_proxy这个环境变量来设置代理服务器，所以在linux下只要设置了这个环境变量就能被这些软件识别，而对于代理服务器用什么协议都行，比如使用http协议或者socks协议等。

那么对于一些比如chrome和yum这些针对http_proxy可能不会生效，比如chrome用的是server_proxy这个变量，而且是在启动时设置才生效。

| 环境变量    | 描述                                                         | 值示例                                                       |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| http_proxy  | 为http变量设置代理；默认不填开头以http协议传输               | 10.0.0.51:8080 user:pass@10.0.0.10:8080 socks4://10.0.0.51:1080 socks5://192.168.1.1:1080 |
| https_proxy | 为https变量设置代理；                                        | 同上                                                         |
| ftp_proxy   | 为ftp变量设置代理；                                          | 同上                                                         |
| all_proxy   | 全部变量设置代理，设置了这个时候上面的不用设置               | 同上                                                         |
| no_proxy    | 无需代理的主机或域名； 可以使用通配符； 多个时使用“,”号分隔； | *.aiezu.com,10.*.*.*,192.168.*.*, *.local,localhost,127.0.0.1 |

写入如下配置：

```
export proxy="http://192.168.5.14:8118"
export http_proxy=$proxy
export https_proxy=$proxy
export ftp_proxy=$proxy
export no_proxy="localhost, 127.0.0.1, ::1"
```

而对于要取消设置可以使用如下命令，其实也就是取消环境变量的设置：

```
unset http_proxy
unset https_proxy
unset ftp_proxy
unset no_proxy
```