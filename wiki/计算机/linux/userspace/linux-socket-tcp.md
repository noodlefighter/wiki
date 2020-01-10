

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

