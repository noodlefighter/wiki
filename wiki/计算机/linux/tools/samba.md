

---

## samba文件服务配置

```

/etc/samba/smb.conf   　　　　　　 　　　　　　　　　#samba服务的主要配置文件
/var/log/samba         　　　　　　　　  　　　　　　#samab服务存放日志文件

```





## smbclient 工具

smbget 下载文件：

```
$ smbget smb://192.168.99.2/软件部/resources/README.txt --user=user%passwd
```

smbclient 交互式访问服务器：

```
$ smbclient //192.168.99.2/软件部 passwd -U user
```

