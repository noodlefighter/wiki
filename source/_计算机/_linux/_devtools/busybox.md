

---

## DHCP客户端udhcpc

busybox自带个简单的dhcp client，获取到IP后会执行脚本进行配置，编辑`/usr/share/udhcpc/default.script`，记得给+x权限：

```bash
#!/bin/sh

#script edited by Tim Riker <Tim@Rikers.org>

[ -z "$1" ] && echo "Error: should be called from udhcpc" && exit 1

RESOLV_CONF="/etc/resolv.conf"
[ -n "$broadcast" ] && BROADCAST="broadcast $broadcast"
[ -n "$subnet" ] && NETMASK="netmask $subnet"

case "$1" in
  deconfig)
    /sbin/ifconfig $interface 0.0.0.0
    ;;

  renew|bound)
    /sbin/ifconfig $interface $ip $BROADCAST $NETMASK

    if [ -n "$router" ] ; then
      echo "deleting routers"
      while route del default gw 0.0.0.0 dev $interface ; do
        :
      done

      for i in $router ; do
        route add default gw $i dev $interface
      done
    fi

    echo -n > $RESOLV_CONF
    [ -n "$domain" ] && echo search $domain >> $RESOLV_CONF
    for i in $dns ; do
      echo adding dns $i
      echo nameserver $i >> $RESOLV_CONF
    done
    ;;
esac

exit 0
```

执行结果：
```
~ # udhcpc
udhcpc (v1.20.2) started
Sending discover...
Sending select for 192.168.1.68...
Lease of 192.168.1.68 obtained, lease time 86400
deleting routers
route: SIOCDELRT: No such process
adding dns 192.168.2.1
adding dns 192.168.2.1
~ # ifconfig
eth0      Link encap:Ethernet  HWaddr 00:E0:4C:36:04:71
          inet addr:192.168.1.68  Bcast:192.168.3.255  Mask:255.255.252.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:70680 errors:0 dropped:51 overruns:0 frame:0
          TX packets:10 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:4522321 (4.3 MiB)  TX bytes:2728 (2.6 KiB)
```