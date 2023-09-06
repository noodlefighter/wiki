## tailscale直连

tailscale由wireguard实现，所以如果连接的双方中有一方将UDP端口暴露在公网中，就可以直连，否则流量将被转发，增加延迟。

用`tailscale status`命令可以看是直连还是转发：

```
$ tailscale status
100.126.218.41  ser770294326422      abc@   linux   -
100.73.43.142   r-store              abc@   linux   active; direct 182.88.46.110:22386, tx 114152 rx 112744
100.73.31.71    r-ddk                abc@   linux   active; relay "tok", tx 99882192 rx 449687764
```

`direct`字样是直连；`relay`字样为通过DREP节点转发。



如果需要指定暴露的端口，可在启动服务增加参数，如改成38892：

```
/usr/sbin/tailscaled --port=38892
```

如debian下可以改服务文件`/lib/systemd/system/tailscaled.service`里的端口号实现。



相关概念：

- Headscale: tailscale的一个开源服务控制器实现
- DERP：tailscale的中继服务器，自创协议
- STUN：Session Traversal Utilities for NAT，NAT会话穿越应用程序，就是打洞服务



## 自建Custom DERP节点，自定义STUN和DREP服务端口

前提：

- 我这里用的NAT VPS， 就是那种免备案的巨便宜的，一台机只给你在公网IP上挂10个端口转发的VPS，所以必须自定义端口
- DERP是中转服务，TCP，在HTTP协议的基础上转发流量，
- STUN是打洞服务，UDP，
- 有自己的域名，下文都是xxxxx.com

Step1. 给域名申请SSL证书，最简单是用`acme.sh`申请，我的域名挂在cloudflare上，用DNS API的方式最简单：

```
  export CF_Key="XXXXX"
  export CF_Email="XXXXXX"
  acme.sh --set-default-ca --server https://acme-v02.api.letsencrypt.org/directory
  acme.sh  --issue  -d xxxxxx.com --dns dns_cf
```

> cloudflare如何拿API KEY？
>
> - 登入后，右上角My Profile
> - 左侧API Tokens
> - 添加KEY；如果已经有KEY了就在“Global API Key”右边点“View”查看

Step2. 建一个derp服务的目录，把证书复制进来：

```
mkdir derper && cd derper
mkdir certs
acme.sh --install-cert -d xxxx.com --cert-file ./certs/xxxx.com.crt --key-file ./certs/xxxx.com.key
acme.sh --install-cert -d derp.1000bug.com --cert-file ./certs/derp.1000bug.com.crt --key-file ./certs/derp.1000bug.com.key
```

Step3.开启DERP服务，使用网友现成的Dockerfile，这里用docker-compose，新建`docker-compose.yml`：

```
version: '3.5'
services:
  derper:
    container_name: derper
    image: fredliang/derper
    restart: always
    ports:
      - "3478:38893/udp" # STUN服务
      - "38894:38894" # DERP服务
    volumes:
      - /home/r/derper/certs:/app/certs    
    command: /app/derper --hostname=xxx.com --certmode=manual --certdir=/app/certs/ --a=:38894 --stun=true --stun-port=38893
```

Step4. 编辑tailscale的线上ACL配置，添加

```
	"derpMap": {
		"Regions": {
			"900": {
				"RegionID":   900,
				"RegionCode": "cn",
				"RegionName": "My CN Dreper",
				"Nodes": [
					{
						"Name":     "1",
						"RegionID": 900,
						"HostName": "xxxx.com",
						"STUNPort": 38893,
						"STUNOnly": false,
						"DERPPort": 38894,				
					},
				],
			},
		},
	},
```

执行`docker-compose up`（调通之后，后台运行可以加`-d`参数）：

```
$ docker-compose up
Recreating derper ... done
Attaching to derper
derper    | 2023/09/06 05:40:22 no config path specified; using /var/lib/derper/derper.key
derper    | 2023/09/06 05:40:22 derper: serving on :38894 with TLS
derper    | 2023/09/06 05:40:22 running STUN server on [::]:38893
```

这时候用浏览器打开`https://xxxx.com:38894`，应该能看到“This is a [Tailscale](https://tailscale.com/) [DERP](https://pkg.go.dev/tailscale.com/derp) server.”的字样，说明服务正常运行了，注意看证书是否被信任。

Step5:验证通讯：

在网络内任一台机`tailscale netcheck`，能看到自己节点的延迟就说明正常，不正常请加`--verbose`：

```
$ tailscale netcheck
Report:
	* UDP: true
	* IPv4: yes, ************8:9003
	* IPv6: yes, [ ************]:47246
	* MappingVariesByDestIP: false
	* HairPinning: false
	* PortMapping:
	* CaptivePortal: false
	* Nearest DERP: My CN Dreper
	* DERP latency:
		- cna: 32.5ms  (My CN Dreper)  <------ 有数字出来才正常
		- tok: 81.9ms  (Tokyo)
		- hkg: 83.2ms  (Hong Kong)
```

再使用`tailscale ping xxx`一台必须使用中继连接的机器，能ping通说明中转节点转发流量了：

```
$ tailscale ping r-store
pong from r-store (100.73.43.142) via DERP(cna) in 69ms
pong from r-store (100.73.43.142) via DERP(cna) in 60ms
```

> 当前，我自己的运行情况，证书还是有问题：
> netcheck正常，ping不正常，用curl访问DERP会提示:curl: (60) SSL certificate problem: unable to get local issuer certificate
> 只有ACL里用加了`InsecureForTests: true`选项流量才能被中转，这个选项关闭了TLS验证



