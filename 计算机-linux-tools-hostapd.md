title: hostapd
date: 2019-08-18
categories:
- 计算机
- linux
- tools


---

hostapd用于开启wifi ap，执行后会创建`/var/run/hostpad`文件夹，`hostapd_cli`是用户操作界面。

```
$ hostapd /etc/hostapd.conf &
$ hostapd_cli -i wlan0 enable
$ hostapd_cli -i wlan0 disable
```

## 用法

```
#!/bin/sh
#
# Start the Hotspot....
#

HOSTAPD_CONF=/etc/hostapd.conf
HOSTAPD_CONF_DEFAULT=/rom${HOSTAPD_CONF}

case "$1" in
  start)
        printf "Starting Hotspot: "
        
        # start hostpad if /var/run/hostapd not exsit
        if ! [ -e /var/run/hostapd ]; then
                hostapd $HOSTAPD_CONF > /dev/null &
                timeout=0
                while ! [ -e /var/run/hostapd ]; do
                        usleep 100000
                        let timeout++                
                        if [ $timeout -gt 10 ]; then
                                 echo "FAIL"
                                 exit 1
                        fi
                done                                                               
        fi
        
        hostapd_cli -i wlan0 enable > /dev/null
        [ $? = 0 ] && echo "OK" || echo "FAIL"
        ;;
  stop)
        printf "Stopping Hotspot: "
        hostapd_cli -i wlan0 disable > /dev/null
        [ $? = 0 ] && echo "OK" || echo "FAIL"
        ;;
  ssid)
        if [ $# == 2 ]; then
                printf "Setting Hotspot SSID: "
                {
                        sed -i "s/^ssid=.*/ssid=$2/" $HOSTAPD_CONF &&
                        hostapd_cli -i wlan0 set ssid "$2" > /dev/null &&
                        echo "OK"
                } || { # error catch
                        echo "FAIL"
                        exit 1
                }
                "$0" stop
                killall hostapd
                "$0" start
        else
                SSID=`hostapd_cli -i wlan0 status | sed -n 's/^ssid\[0\]=\(.*\)/\1/p'`
                [ -n "${SSID}" ] && echo $SSID || exit 1
        fi
        ;;
  passwd)
        if [ $# == 2 ]; then
                printf "Setting Hotspot PASSWD: "
                {
                        sed -i "s/^wpa_passphrase=.*/wpa_passphrase=$2/" $HOSTAPD_CONF &&
                        hostapd_cli -i wlan0 set wpa_passphrase "$2"  > /dev/null &&
                        echo "OK"
                } || { # error catch
                        echo "FAIL"
                        exit 1
                }
                "$0" restart
        else
                exit 1
        fi
        ;;
  reset)
        printf "Resetting Setting Configuration: "
        cp $HOSTAPD_CONF_DEFAULT $HOSTAPD_CONF
        [ $? = 0 ] && echo "OK" || (echo "FAIL"; exit 1)
        "$0" stop
        killall hostapd
        "$0" start
        ;;
  state)
        STATE=`hostapd_cli -i wlan0 status | sed -n 's/^state=\(.*\)/\1/p'`
        [ -n "${STATE}" ] && echo $STATE || exit 1
        ;;
  restart|reload)
        "$0" stop
        "$0" start
        ;;
  *)
        echo "Usage: $0 {start|stop|ssid|passwd|state|reset|restart}"
        exit 1
esac

exit $?

```

## `/dev/random`随机数不工作导致hostapd的密码错误的问题

现象：开启WEP加密后，密码错误：

```
random: Cannot read from /dev/random: Resource temporarily unavailable
random: Only 0/20 bytes of strong random data available from /dev/random
random: Not enough entropy pool available for secure operations
```

里面的`0/20`，多连几次可能会增加（如变成`7/20`/`14/20`），所以可能多连接几次就能连接成功了。

临时解决办法，用`/dev/urandom`替代：

```
$ mv /dev/random /dev/random.orig
$ ln -s /dev/urandom /dev/random
```

