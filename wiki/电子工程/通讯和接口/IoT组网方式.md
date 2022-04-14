

---

> TODO 继续整理、拆分

## 概念

### LR-WPAN
低速无线个域网

### REST架构
表述性状态传递（Representational State Transfer）
Roy Fielding博士提出的软件架构风格，网络应用的设计开发，降低开发的复杂性，提高系统的可伸缩性
是一组架构约束条件和原则
似乎核心思想是：通过URL设计Web系统

[参考](http://baike.baidu.com/link?url=lN1LXWoHNOhpSPbXah3JCFTN5CZb6j090JtBz75FHIkjOMzu2yQHKw_wztkXYfLplfP3fg3xttNK0AKWbTx85q)

相关：另外两种主流Web服务方案为SOAP和XML-RPC

## 规范&协议
### 802.15.4
规定了物理层phy和媒体访问控制层mac

### 6LoWPAN
802.15.4 + IPv6

* 低速率，对于2.4GHz、828MHz、915MHz 3个频段分别对应250Kb/s、20Kb/s和40Kb/s3种速率
* 低功耗，在待机模式下可使用2节5号干电池驱动6个月以上
* 低成本，一般采用硬件资源非常有限的底端嵌入式设备或更小的特殊设备
* 短距离，节点信号覆盖范围有限，一般为10－100m
* 低复杂度，比现有的标准低；⑥短帧长，最大帧长度为127字节
* 多拓扑，网络拓扑结构丰富，支持星型拓扑和点对点拓扑2种基本拓扑结构及其混合组网。
[来源](http://www.elecfans.com/news/wangluo/20141010355885.html)

### CoAP
http://coap.technology/

6LowPAN协议栈的应用层协议 替代http
最小数据包仅4byte 运行在UDP上
[参考](http://network.chinabyte.com/333/13351333.shtml)

相关开源库 
[libcoap ](https://github.com/obgm/libcoap): A CoAP (RFC 7252) implementation in C, simplifiedBSD可商用.

### TLS
Transport Layer Security 安全传输层协议
安全传输层协议（TLS）用于在两个通信应用程序之间提供保密性和数据完整性。该协议由两层组成： TLS 记录协议（TLS Record）和 TLS 握手协议（TLS Handshake）。较低的层为 TLS 记录协议，位于某个可靠的传输协议（例如 TCP）上面，与具体的应用无关，所以，一般把TLS协议归为传输层安全协议。
[来源](http://baike.baidu.com/link?url=9fjHUJTlF1GOaVe-GhRvUCQRIvOPw_imDfNkzK18cX4QsHgkwDw2TNERR3tayelAgh1Op5kYf25d3gh8CDlx9a)

相关开源库 
[s2n](https://github.com/awslabs/s2n)


### DTLS

### MQTT

### LWM2M

### NB-IoT
Narrow Band Internet of Things
蜂窝窄带物联网
