

---



## 服务器配置：

```
# apt install nfs-kernel-server
# vi 
```

编辑配置`/etc/exports`：
```
/home/dev/workspaces/hi3516a/nfs        (rw,sync,no_subtree_check)
```

挂载：
```
mount -t -o nfs localhost:/home/dev/workspaces/hi3516a/nfs /mnt/nfs
```

## 错误记录

```
svc: failed to register lockdv1 RPC service (errno 111)
加个-o nolock
```