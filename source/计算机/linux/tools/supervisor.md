---

守护进程管理工具Supervisor

轻松管理守护进程，就算挂了也可以被拉起来。

例子，`/etc/supervisor/conf.d/ss.conf`

```none
[program:ss-server]
command=ss-server -c /etc/shadowsocks-libev/config.json
directory=/home
environment=环境变量A="";环境变量B=""
stdout_logfile_maxbytes=20MB
stdout_logfile=/var/log/supervisor/%(program_name)s.log
stderr_logfile_maxbytes=20MB
stderr_logfile=/var/log/supervisor/%(program_name)s.log
autostart=true
autorestart=true
startsecs=5
priority=1
stopsignal=HUP
stopasgroup=true
killasgroup=true
```



命令

```
superviosrctl 交互式
supervisord 守护程序
```