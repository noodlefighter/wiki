

## curl 下载文件

```
$ curl -LJO http://192.168.99.13:9999/raspi-202103131555.tar.gz
```



## curl HTTP POST测试

POST json：

```
$ curl -X POST -H "Content-Type: application/json" http://localhost:8080/rpc -d '{}'
```

