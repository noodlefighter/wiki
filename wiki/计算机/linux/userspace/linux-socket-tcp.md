

---



## linux tcp客户端示例代码



```
	struct sockaddr_i n servaddr;
	int ret, flags;

	ble_agent_sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (ble_agent_sockfd == -1) {
		LOG_ERR("%s: socket creation failed...\n", __func__);
		return -1;
	}

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family      = AF_INET;
	servaddr.sin_port        = htons(LOCAL_SERVER_PORT);
	servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
	ret = connect(ble_agent_sockfd, (struct sockaddr*)&servaddr, sizeof(struct sockaddr));
	if (0 != ret) {
		LOG_ERR("%s: connect failed, %d\n", __func__, ret);
		return ret;
	}

	// set no-block mode
	flags = fcntl(ble_agent_sockfd, F_GETFL, 0);
	ret = fcntl(ble_agent_sockfd, F_SETFL, flags | O_NONBLOCK);
	if (0 != ret) {
		LOG_ERR("%s: fcntl() failed, %d\n", __func__, ret);
		return ret;
	}
```



## 错误：“bind() fail, Address already in use”

用`netstat`命令即可知道情况，可能是：

1. 已经有程序使用这个端口了；

2. 端口处于`close_wait`状态，参考https://web.archive.org/web/20170113135705/http://unix.derkeiler.com/Mailing-Lists/SunManagers/2006-01/msg00367.html，可能是因为连接已经FIN但应用程序没有响应并close掉fd；

3. 程序可能处于 `time_wait` 状态，可以等，或者用 `SO_REUSEADDR`（似乎不管用）；`/proc/sys/net/ipv4/tcp_fin_timeout`；或者设置`SO_LINGER`（似乎有效）：

   ```
   struct linger sl;
   sl.l_onoff = 1;		/* non-zero value enables linger option in kernel */
   sl.l_linger = 0;	/* timeout interval in seconds */
   setsockopt(sockfd, SOL_SOCKET, SO_LINGER, &sl, sizeof(sl));
   ```



## socket keepalive的opt设置

```
  setsockopt(_nSock, SOL_SOCKET, SO_KEEPALIVE, (void *)&keepAlive, sizeof(keepAlive));
  setsockopt(_nSock, SOL_TCP, TCP_KEEPIDLE, (void*)&keepIdle, sizeof(keepIdle));
  setsockopt(_nSock, SOL_TCP, TCP_KEEPINTVL, (void *)&keepInterval, sizeof(keepInterval));
  setsockopt(_nSock, SOL_TCP, TCP_KEEPCNT, (void *)&keepCount, sizeof(keepCount));
  int flags  = fcntl(_nSock,F_GETFL,0);
  logger->debug("SocketIO::connect flag:%d",flags);
  fcntl(_nSock,F_SETFL,flags&~O_NONBLOCK);
```



## socket 指定网卡发包

```
#include <net/if.h>

struct ifreq ifr;
memset(&ifr, 0x00, sizeof(ifr));
strncpy(ifr.ifr_name, interface, strlen(interface));
setsockopt(_nSock, SOL_SOCKET, SO_BINDTODEVICE, (char *)&ifr, sizeof(ifr));
```



## 阻塞式socket设置超时时间



```
  {
    int ret = 0;
    struct timeval timeout;
    timeout.tv_sec = 5;
    timeout.tv_usec = 0;
    socklen_t len = sizeof(timeout);
    do {
      ret = setsockopt(_nSock, SOL_SOCKET, SO_SNDTIMEO, &timeout, len);
      CC_BREAK_IF(ret < 0);
      ret = setsockopt(_nSock, SOL_SOCKET, SO_RCVTIMEO, &timeout, len);
      CC_BREAK_IF(ret < 0);
    } while(0);
    if (ret < 0) {
        logger->error("Error when setsockopt: [%d]%s", errno, strerror(errno));
        return FALSE;
    }
  }
```

