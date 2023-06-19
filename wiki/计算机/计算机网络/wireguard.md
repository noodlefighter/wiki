## WireGuard配置例

因为家庭宽带没有IPv4，买了个NAT-VPS做流量转发，VPS仅有IPv4地址+10个端口，所以方案选用WireGuard建VPN，与NAS互通，以下简称wg。

wg的配置涉及到的概念：

Interface，本机接口
- 私钥，本机的私钥
- Address：本机在wg网络中的地址
- ListenPort：监听的端口，不指定就随机，如果做服务端就应该指定，让其他peer指定Endpoint时带上这个端口

Peer，wg不分服务端、客户端，peer就是本机以外的其他节点
- 公钥，目标节点的公钥
- Endpoint，peer对应的主机，可以写作`39.156.66.10:5432`
- 允许的IP，允许该 Peer 在隧道中使用的 IP段，通常是该 Peer 的隧道 IP 地址和通过隧道的路由网络，客户端可能会根据这个选项自动设置路由表



WireGuard需要用到内核特性，Linux 5.6以后自带，而这之前需要安装内核模块，比如在ubuntu上是`wireguard-dkms`这个包，以及工具`wireguard-tools`



**VPS上配置**

先生成公私钥：

```
wg genkey | tee wg0-prikey | wg pubkey > wg0-pubkey
```

配置`/etc/wireguard/wg0.conf`

```
[Interface]
Address = 10.10.10.1/24
ListenPort = 5432（因为本机有IPv4公网地址，所以需要暴露明确的端口）
PrivateKey = (VPS的私钥)

[Peer]
PublicKey = （写NAS的公钥）
AllowedIPs = 10.10.10.2/32（这里就一台机器，直接写死NAS地址）
PersistentKeepalive = 25
```

开启：

```
$ wg-quick up wg0
```



**NAS上配置**

一样要先生成公私钥，然后配置`/etc/wireguard/wg0.conf`

```
[Interface]
Address = 10.10.10.2/24
PrivateKey = (NAS的私钥)

[Peer]
Endpoint = （VPS的IP）:5432
AllowedIPs = 10.10.10.1/32（直接写死VPS的IP地址）
PublicKey = （写VPS的公钥）
PersistentKeepalive = 25
```

开启即可，应该就可以相互ping通了，如果不通，可以在两端分别用`wg`命令看当前状态，例如：

```
interface: wg0
  public key: 5MQ48dLW/ngQCd7WcHYGzDCt5G6UbDwnpFyWY0He/Dg=
  private key: (hidden)
  listening port: 42791

peer: hJkRu0eHnzstHTpuACPTDQ83S6QuZ/vU9rMLE5IVkUw=
  endpoint: (..VPS的IP..):5432
  allowed ips: 10.10.10.1/32
  latest handshake: 46 seconds ago
  transfer: 2.86 MiB received, 145.47 MiB sent
  persistent keepalive: every 25 seconds
```

