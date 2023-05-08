## TCP/IP组播

> 1. 组播地址的范围：组播地址是IPv4地址中的一个特殊范围，它的范围是224.0.0.0到239.255.255.255。其中，224.0.0.0到224.0.0.255是组播地址的固定范围，称为“本地组播地址”（Local Scope Multicast Address），用于在一个局域网或广域网中进行组播通信。
> 2. 组播地址的分类：组播地址可以按照用途和范围进行分类。其中，224.0.0.0到224.0.0.255是预留的组播地址，用于特定用途；224.0.1.0到238.255.255.255是全局范围的组播地址，可以在任何地方使用；239.0.0.0到239.255.255.255是本地管理员范围的组播地址，用于在特定子网中进行组播通信。

网卡设置：

````
sudo ip link set dev enp2s0 multicast on
sudo ip addr add 224.0.0.0/24 dev enp2s0 
````

测试接收组播：

```
socat UDP4-RECVFROM:5000,ip-add-membership=224.0.0.2:0.0.0.0 STDOUT
```

测试发送组播：

```
echo "Hello, multicast!" | socat - UDP4-DATAGRAM:224.0.0.2:5000,broadcast
```

## 组播发送接收DEMO

> via: https://www.cnblogs.com/lifan3a/articles/6780765.html

组播server，发送组播数据的例子


实现组播数据包发送的步骤如下：
创建AF_INET, SOCK_DGRAM的socket。
用组播IP地址和端口初始化sockaddr_in类型数据。
IP_MULTICAST_LOOP，设置本机是否作为组播组成员接收数据。
IP_MULTICAST_IF，设置发送组播数据的端口。
发送组播数据。


有注释代码：

```
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>


struct in_addr localInterface;
struct sockaddr_in groupSock;
int sd;
char databuf[1024] = "Multicast test message lol!";
int datalen = sizeof(databuf);


int main (int argc, char *argv[ ])
{
     sd = socket(AF_INET, SOCK_DGRAM, 0);
     if(sd < 0) {
          perror("Opening datagram socket error");
          exit(1);
     } else
          printf("Opening the datagram socket...OK.\n");


     memset((char *) &groupSock, 0, sizeof(groupSock));
     groupSock.sin_family = AF_INET;
     groupSock.sin_addr.s_addr = inet_addr("226.1.1.1");
     groupSock.sin_port = htons(4321);


     localInterface.s_addr = inet_addr("203.106.93.94");
     if(setsockopt(sd, IPPROTO_IP, IP_MULTICAST_IF, (char *)&localInterface, sizeof(localInterface)) < 0) {
        perror("Setting local interface error");
        exit(1);
     } else
        printf("Setting the local interface...OK\n");


     if(sendto(sd, databuf, datalen, 0, (struct sockaddr*)&groupSock, sizeof(groupSock)) < 0) {
        perror("Sending datagram message error");}
     else
        printf("Sending datagram message...OK\n");


     return 0;
}

```

**组播**client，接收组播数据的例子


创建AF_INET, SOCK_DGRAM类型的socket。
设定 SO_REUSEADDR，允许多个应用绑定同一个本地端口接收数据包。
用bind绑定本地端口，IP为INADDR_ANY，从而能接收组播数据包。
采用 IP_ADD_MEMBERSHIP加入组播组，需针对每个端口采用 IP_ADD_MEMBERSHIP。
接收组播数据包。

有注释的代码：

```
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


struct sockaddr_in localSock;
struct ip_mreq group;
int sd;
int datalen;
char databuf[1500];


int main(int argc, char *argv[])
{
    sd = socket(AF_INET, SOCK_DGRAM, 0);
    if(sd < 0){
        perror("Opening datagram socket error");
        exit(1);
    } else
        printf("Opening datagram socket....OK.\n");
  
    {
        int reuse = 1;
        if(setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, (char *)&reuse, sizeof(reuse)) < 0){
            perror("Setting SO_REUSEADDR error");
            close(sd);
            exit(1);
        } else
            printf("Setting SO_REUSEADDR...OK.\n");
    }


    memset((char *) &localSock, 0, sizeof(localSock));
    localSock.sin_family = AF_INET;
    localSock.sin_port = htons(49500);
    localSock.sin_addr.s_addr = INADDR_ANY;
    if(bind(sd, (struct sockaddr*)&localSock, sizeof(localSock))){
        perror("Binding datagram socket error");
        close(sd);
        exit(1);
    } else
        printf("Binding datagram socket...OK.\n");
  
    group.imr_multiaddr.s_addr = inet_addr("227.0.0.25");
    group.imr_interface.s_addr = inet_addr("150.158.231.2");
    if(setsockopt(sd, IPPROTO_IP, IP_ADD_MEMBERSHIP, (char *)&group, sizeof(group)) < 0){
        perror("Adding multicast group error");
        close(sd);
        exit(1);
    } else
        printf("Adding multicast group...OK.\n");
  
    datalen = sizeof(databuf);
    if(read(sd, databuf, datalen) < 0){
        perror("Reading datagram message error");
        close(sd);
        exit(1);
    } else {
        printf("Reading datagram message...OK.\n");
        printf("The message from multicast server is: %d\n", datalen);
    }


    return 0;
}
```


注意：接收**[组播](http://blog.csdn.net/shanzhizi/article/category/1157892)**的网络端口需要设定一个IP地址，我调试的计算机有两个端口，我在第二个端口上接收组播，开始没有设定这个端口的IP地址，只是给出了组播路由到第二个端口，结果死活收不到数据，后来设了一个IP地址就ok了