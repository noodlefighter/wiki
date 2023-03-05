

### openssh工具集

```
# 服务端
sshd            SSH 服务端程序
sftp-server     SFTP服务端程序
ssh-agent       ssh代理程序

# 客户端
ssh             SSH协议的客户端程序，用来登入远程系统或远程执行命令
slogin          ssh的别名
scp             文件传输客户端
sftp            交互式sftp-server客户端，用法和ftp命令一样。

# 秘钥管理
ssh-add         SSH代理相关程序，用来向SSH代理添加dsa　key
ssh-keygen      生成ssh公私钥
ssh-keyscan     从其他主机上收集公钥
```
## OpenSSH秘钥默认路径、权限设置、文件格式参考

目录为`~/.ssh`，权限700。

私钥大概长这样，权限600。

```none
-----BEGIN RSA PRIVATE KEY-----
MIIEoQIBAAKCAQEAiAbdVhzD0c+sWV2nMFIH9vA1z/zCTlti3EDoWFG9lGjyCjL2
....
wZMCgYBTglrAaucwtSgkPEuLXfiTIVGuobR3eQxOD19T+0uC16ddXsXiBSYOGH+w
xgc+HU3ShNo9N1jIusuXJatXWL+MyUjpOWUtSre748duWd531UAHOIXPAHBdv5o2
zgtiENtUwccic/HDVMl8i2K7cYocFE9Iem8wXoYz/eI/QM9vSA==
​-----END RSA PRIVATE KEY-----
```

```

默认路径：
​```c
mv ssh_private_key ~/.ssh/id_dsa
```

公钥位置在`~/.ssh/authorized_keys`，权限600。

大概长这样
```none
ssh-rsa AAAAB3Nza.....F1Yatzmw==
ssh-rsa AAAAB3Nza.....1+tinL1aWB/XgJQ==
```

临时指定某ssh-key用于建立ssh连接：

```
$ ssh-agent
$ ssh-add ~/.ssh/xxxx
$ ssh user@xxx.com
```



## 不同的ssh服务器，自动使用不同的密钥

```
$ cd ~/.ssh
$ touch config
$ nano config
```

```
Host exist_server
    HostName exist_server_IP/exist_server_domain
    IdentityFile ~/.ssh/id_rsa_exist_server
    PreferredAuthentications publickey
    User username

Host github.com
    HostName github.com
    IdentityFile ~/.ssh/id_rsa_github
    PreferredAuthentications publickey
    User github_username
```



## sshfs

sshfs可以挂在一个sftp中的目录到本地路径上：

```
mkdir -p /mnt/mysdk

# 所有用户均可访问
sudo sshfs -o allow_other user@xxx.xxx.xxx.xxx:/home/mpc/workspaces /mnt/mysdk

# 仅当前用户访问
sshfs user@xxx.xxx.xxx.xxx:/home/mpc/workspaces ~/mysdk
```

似乎没法用sshpass在这个命令上



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



## ssh代理 ssh隧道 ssh跳板

> via: [利用SSH代理访问内网资源](https://blog.dteam.top/posts/2017-07/%E5%88%A9%E7%94%A8ssh%E4%BB%A3%E7%90%86%E8%AE%BF%E9%97%AE%E5%86%85%E7%BD%91%E8%B5%84%E6%BA%90.html)

```
SSH的-L与-D代理
SSH有三种代理参数-L,-D,-R。-R代理不是本次重点，有兴趣的读者可以自行查阅man手册。

-L参数会在本地监听一个端口，转发数据到远程主机上。 ssh -NL 3306:localhost:3306 user@remote_ip 在本地监听一个3306端口，转发到远程主机上的localhost:3306上，等于访问本地的3306端口就相当于访问到了远程的mysql服务。这种方式访问远程服务会更安全，远程服务不需要对外网暴露端口。 很明显，这个代理只适用于代理单一ip单一服务的需求有用，本质上是反向代理，客户端不需要额外配置。
-D参数就厉害了，在本地开放一个socks5协议的代理端口，利用这个端口可以动态的访问到远程内网的环境。 ssh -ND 1080 user@remote_ip 这条命令会在本地开放一个1080的socks5端口，支持socks5协议代理的应用程序就可以利用这个端口直接访问到内网资源。比如: curl –socks5 127.0.0.1:1080 localhost 让curl命令利用socks5协议代理访问到远程服务器上的http服务，浏览器直接配置这个代理服务就可以无阻碍的访问到内网中所有的http服务了。 很明显，这个代理本质上是正向代理，可以实现一个代理访问更多服务资源的需求。但是需要客户端本身支持代理。
```

使用ProxyJump实现多级跳

> 来源：https://segmentfault.com/a/1190000020088166

首先是-J选项：

```bash
ssh -J user@jump.tunzao.me:80 user2@a.tunzao.me
```

使用配置的例子，这样可以方便使用scp：

```
### 堡垒机
Host jump
  HostName jump.tunzao.me
  Port 80
  User user

### 目标机器，通过堡垒机登录
Host a
  HostName a.tunzao.me
  ProxyJump  jump
```



## ssh穿透-在docker容器里装git服务器

把git服务器装在docker容器中时，如果要用SSH方式访问git仓库，又不想在使用时指定特殊的端口，就必须与宿主共享22端口。

> 参考：http://www.ateijelo.com/blog/2016/07/09/share-port-22-between-docker-gogs-ssh-and-local-system

- 在真实系统里创建名为`git`的用户
- 把UID和GID传入docker容器，一般是通过参数，在容器内entrypoint接收参数，使用指定UID/GID执行应用，以保证容器中创建的文件与宿主一致
- 配置SSH端口映射，如命令行 `-v ~git/gogs:/data -p 127.0.0.1:10022:22 -p 3000:3000`.
- 创建符号链接 `/home/git/.ssh` 到 `gogs/git/.ssh`
- 生成密钥对，供宿主与容器间通讯
- 执行：

```
mkdir -p /app/gogs/
cat >/app/gogs/gogs <<'END'
#!/bin/bash
GIT_KEY_ID=$(cat /home/git/.ssh/id_rsa.pub | awk '{ print $3 }')
if ! grep -q "no-port.*$GIT_KEY_ID" /home/git/.ssh/authorized_keys
then
    echo \
    "no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty" \
    "$(cat /home/git/.ssh/id_rsa.pub)" \
    >> /home/git/.ssh/authorized_keys
fi
ssh -p 10022 -o StrictHostKeyChecking=no git@127.0.0.1 \
    SSH_ORIGINAL_COMMAND=$(printf '%q' "$SSH_ORIGINAL_COMMAND") "$0" "$@"
END
chmod 755 /app/gogs/gogs
```



原理，在 `~/.ssh/authorized_keys`中：

```
command="/app/gogs/gogs serv key-1 --config='/data/gogs/conf/app.ini'",no-po
rt-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-rsa AAAVFUEV0
SpbdpMBMc.................0ALtpNr6Nc6 gogsuser1@host1
...
command="/app/gogs/gogs serv key-2 --config='/data/gogs/conf/app.ini'",no-po
rt-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-rsa AAAAA34ff
30rV0ay6Q.................hGWhpsqNeuE gogsuser2@host2
```

当有客户使用git用户连接上宿主的ssh，就会执行`/app/gogs/gogs`从而走向代理通道。