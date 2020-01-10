

---

## systemctl

>  systemd 是 Linux 下的一款系统和服务管理器，兼容 SysV 和 LSB 的启动脚本。systemd 的特性有：支持并行化任务；同一时候採用 socket 式与 D-Bus 总线式激活服务；按需启动守护进程（daemon）。利用 Linux 的 cgroups 监视进程；支持快照和系统恢复。维护挂载点和自己主动挂载点。各服务间基于依赖关系进行精密控制

systemd的人机交互接口就是systemctl，比如看nfs服务的日志：

```
$ systemctl status nfs-server.service
```

查找自启服务

```
$ sudo systemctl list-unit-files | grep enabled
```

开机自启

```
$ sudo systemctl enable sshd
```

禁止开机自启

```
$ sudo systemctl disable sshd
```

停止服务

```
$ systemctl stop sshd
```

启动服务

```
$ systemctl start sshd
```

检查某个服务的状态

```
$ systemctl status sshd
```

## 添加一个服务

> https://www.freedesktop.org/software/systemd/man/systemd.service.html#Examples

`/etc/systemd/system/foo.service`，权限644.

```
[Unit]
Description=Foo

[Service]
WorkingDirectory=/usr/local
ExecStart=/usr/sbin/foo-daemon

[Install]
WantedBy=multi-user.target
```

完成后重新载入：

```
$ systemctl daemon-reload
```

