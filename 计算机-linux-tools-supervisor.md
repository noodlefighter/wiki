title: supervisor
date: 2019-06-08
categories:
- 计算机
- linux
- tools


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

注意这里的command，不是命令行，要执行bash命令可以`bash -c "xxxx"`。

环境变量的问题，类似这样解决，详细可以参考`man supervisor`：

```
environment=PYTHONPATH=/opt/mypypath:%(ENV_PYTHONPATH)s,PATH=/opt/mypath:%(ENV_PATH)s
```

## 交互式操作界面

`superviosrctl`命令进入交互式界面，常用命令：`reload`、`status`

