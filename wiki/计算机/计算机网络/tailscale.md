## tailscale直连

tailscale由wireguard实现，所以如果连接的双方中有一方将UDP端口暴露在公网中，就可以直连，否则流量将被转发，增加延迟。

用`tailscale status`命令可以看是直连还是转发：

```
$ tailscale status
100.126.218.41  ser770294326422      abc@   linux   -
100.73.43.142   r-store              abc@   linux   active; direct 182.88.46.110:22386, tx 114152 rx 112744
100.73.31.71    r-ddk                abc@   linux   active; relay "tok", tx 99882192 rx 449687764
```

`direct`字样是直连；`relay`字样为通过DREP节点转发。



如果需要指定暴露的端口，可在启动服务增加参数，如改成38892：

```
/usr/sbin/tailscaled --port=38892
```

如debian下可以改服务文件`/lib/systemd/system/tailscaled.service`里的端口号实现。



相关概念：

- Headscale: tailscale的一个开源服务控制器实现
- DERP：tailscale的中继服务器，自创协议
- STUN：Session Traversal Utilities for NAT，NAT会话穿越应用程序，就是打洞服务