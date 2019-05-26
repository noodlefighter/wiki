

---

## crontab定时任务

编辑配置：
```
crontab -e
```

内容：
```
# 每天02:06重启
06 2 * * * reboot
```