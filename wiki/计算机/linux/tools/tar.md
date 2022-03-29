

## 通过ssh用tar备份rootfs



```
ssh root@192.168.0.108 'tar cpf - --exclude=/proc --exclude=/lost+found --exclude=/mnt --exclude=/sys --exclude=/media /' > rootfs-$(date +%Y%m%d).tar
```

