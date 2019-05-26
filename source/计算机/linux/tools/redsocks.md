---

## redsocks教程

> 转载自：http://www.h1z166.com/articles/2017/08/21/1503247650811.html

严格意义上来说，proxychains不算自动的全局代理，有没有像Proxifier这样，开了之后自动让所有启动的程序都走系统代理呢？答案就是redsocks。
首先安装Ubuntu编译环境和必要的库：
sudo apt-get install autoconf automake libtool libevent-dev g++
下载源代码，然后编译安装：
./mkauto.sh
cp redsocks /usr/local/bin/
配置文件为：
base { 
// debug: connection progress & client list on SIGUSR1 
log_debug = off;
// info: start and end of client session 
log_info = off;
/* possible `log' values are: 
* stderr 
* file:/path/to/file 
* syslog:FACILITY facility is any of "daemon", "local0"..."local7" 
*/ 
log = "file:/dev/null"; 
// log = stderr; 
// log = "file:/path/to/file"; 
// log = "syslog:local7";
// detach from console 
daemon = on;
/* Change uid, gid and root directory, these options require root 
* privilegies on startup. 
* Note, your chroot may requre /etc/localtime if you write log to syslog. 
* Log is opened before chroot & uid changing. 
*/ 
// user = nobody; 
// group = nobody; 
// chroot = "/var/chroot";
/* possible `redirector' values are: 
* iptables - for Linux 
* ipf - for FreeBSD 
* pf - for OpenBSD 
* generic - some generic redirector that MAY work 
*/ 
redirector = iptables; 
}
redsocks { 
/* `local_ip' defaults to 127.0.0.1 for security reasons, 
* use 0.0.0.0 if you want to listen on every interface. 
* `local_*' are used as port to redirect to. 
*/ 
local_ip = 127.0.0.1; 
local_port = 12345;
// `ip' and `port' are IP and tcp-port of proxy-server 
ip = 127.0.0.1; 
port = 7070;
// known types: socks4, socks5, http-connect, http-relay 
type = socks5;
// login = "foobar"; 
// password = "baz"; 
}
redudp { 
// `local_ip' should not be 0.0.0.0 as it's also used for outgoing 
// packets that are sent as replies - and it should be fixed 
// if we want NAT to work properly. 
local_ip = 127.0.0.1; 
local_port = 10053;
// `ip' and `port' of socks5 proxy server. 
ip = 10.0.0.1; 
port = 1080; 
login = username; 
password = pazzw0rd;
// kernel does not give us this information, so we have to duplicate it 
// in both iptables rules and configuration file. By the way, you can 
// set `local_ip' to 127.45.67.89 if you need more than 65535 ports to 
// forward ;-) 
// This limitation may be relaxed in future versions using contrack-tools. 
dest_ip = 8.8.8.8; 
dest_port = 53;
udp_timeout = 30; 
udp_timeout_stream = 180; 
}
dnstc { 
// fake and really dumb DNS server that returns "truncated answer" to 
// every query via UDP, RFC-compliant resolver should repeat same query 
// via TCP in this case. 
local_ip = 127.0.0.1; 
local_port = 5300; 
}
// you can add more `redsocks' and `redudp' sections if you need.
这里的配置没有配置udp的代理部分，只是配置了tcp即redsocks部分。监听端口是12345。日志关闭了，因为好像我下载的当前版本无论怎么样都产生一堆调试日志，不知道以后会不会修复这点。
启动关闭脚本redsocks.sh为（via）：
#! /bin/bash
SSHHOST=creke 
SSHPORT=22 
SSHUSR=creke 
SSHPWD=creke
SSHDAEMON=/usr/local/bin/plink 
SSHPIDFILE=/var/run/sshtunnel.pid
start_ssh() 
{ 
    echo "Start SSH Tunnel Daemon: " 
    start-stop-daemon -b -q -m -p $SSHPIDFILE --exec $SSHDAEMON -S \ 
    -- -N -D 127.0.0.1:7070 -P $SSHPORT -pw $SSHPWD $SSHUSR@$SSHHOST 
    echo "SSH Tunnel Daemon Started." 
}
stop_ssh() 
{ 
    #ps aux|grep "ssh -NfD 1234"|awk '{print $2}'|xargs kill 
    if [ -f $SSHPIDFILE ]; then 
    PID=$(cat $SSHPIDFILE) 
    kill $PID 
    while [ -d /proc/$PID ]; 
    do 
    sleep 1 
    done 
    fi 
    rm -rf $SSHPIDFILE 
    echo "SSH Tunnel Daemon Stoped." 
}
case "$1" in 
  start) 
    start_ssh 
    cd /usr/local/redsocks 
    if [ -e redsocks.log ] ; then 
      rm redsocks.log 
    fi 
    ./redsocks -p /usr/local/redsocks/redsocks.pid #set daemon = on in config file 
    # start redirection 
    # iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDIRECT --to 12345 
    # iptables -t nat -A OUTPUT -p tcp --dport 443 -j REDIRECT --to 12345 
    # Create new chain 
    iptables -t nat -N REDSOCKS
    # Ignore LANs and some other reserved addresses. 
    iptables -t nat -A REDSOCKS -d 0.0.0.0/8 -j RETURN 
    iptables -t nat -A REDSOCKS -d 10.0.0.0/8 -j RETURN 
    iptables -t nat -A REDSOCKS -d 127.0.0.0/8 -j RETURN 
    iptables -t nat -A REDSOCKS -d 169.254.0.0/16 -j RETURN 
    iptables -t nat -A REDSOCKS -d 172.16.0.0/12 -j RETURN 
    iptables -t nat -A REDSOCKS -d 192.168.0.0/16 -j RETURN 
    iptables -t nat -A REDSOCKS -d 224.0.0.0/4 -j RETURN 
    iptables -t nat -A REDSOCKS -d 240.0.0.0/4 -j RETURN
    # Anything else should be redirected to port 12345 
    iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 12345 
    # Any tcp connection should be redirected. 
    iptables -t nat -A OUTPUT -p tcp -j REDSOCKS 
    ;;
  stop) 
    stop_ssh 
    cd /usr/local/redsocks 
    if [ -e redsocks.pid ]; then 
      kill `cat redsocks.pid` 
      rm redsocks.pid 
    else 
      echo already killed, anyway, I will try killall 
      killall -9 redsocks 
    fi 
    # stop redirection 
    iptables -t nat -F OUTPUT 
    iptables -t nat -F REDSOCKS 
    iptables -t nat -X REDSOCKS 
    ;;
  start_ssh) 
    start_ssh 
    ;;
  stop_ssh) 
    stop_ssh 
    ;;
  clean_dns) 
    # iptables -A INPUT -p udp --sport 53 -m state --state ESTABLISHED -m you-know-who -j DROP -m comment --comment "drop you-know-who dns hijacks" 
    echo this function not finished 
    ;;
  *) 
    echo "Usage: redsocks start|stop|start_ssh|stop_ssh|clean_dns" >&2 
    exit 3 
    ;; 
esac
iptables的规则是让所有的TCP包都发送到redsocks监听的端口12345。本脚本还整合了ssh的daemon启动，使用start-stop-daemon来实现。
启动和关闭：
将启动关闭脚本中的开头的几个变量配置好
启动命令：sudo ./redsocks.sh start
关闭命令：sudo ./redsocks.sh stop

