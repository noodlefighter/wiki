

---



## sshfs

sshfs可以挂在一个sftp中的目录到本地路径上：

```
mkdir -p /mnt/mysdk
sudo sshfs -o allow_other user@xxx.xxx.xxx.xxx:/home/mpc/workspaces /mnt/mysdk
```

## sshpass

ssh不允许在参数里带密码，sshpass能加个-p参数带上密码。

例子，ssh免输入密码远程执行命令：
```
sshpass -p "123456" ssh root@xxx.xxx.xxx.xxx "pwd;"
```

## ssh保持会话

```bash

ServerAliveInterval 60 ＃client每隔60秒发送一次请求给server，然后server响应，从而保持连接

ServerAliveCountMax 3  ＃client发出请求后，服务器端没有响应得次数达到3，就自动断开连接，正常情况下，server不会不响应
```