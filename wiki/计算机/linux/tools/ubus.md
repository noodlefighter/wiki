

ubus是openwrt中替代dbus的小型化的系统内部总线，以便应用间互相调用。

- 很轻量
- 用json交互数据
- 仅适合小数据传输

ubus参考：https://openwrt.org/docs/techref/ubus

## Usage

```
列出所有path
$ ubus list -v
调用
$ ubus call <path> <method> [<message>]
dump
$ ubus monitor
```



## 通过HTTP访问ubus

用到uhttpd、rpcd：

- rpcd在ubus上注册session服务，通过这个服务实现鉴权
- uhttpd对外提供http服务，连接ubus的功能通过`uhttpd_ubus.so`插件提供

配置实例：

/etc/config/rpcd:

```
config login
	option username 'root'
	option password '$p$root'
	list read '*'
	list write '*'
```

/usr/share/rpcd/acl.d/unauthenticated.json:

```
{
    "unauthenticated": {
        "description": "Access controls for unauthenticated requests",
        "read": {
            "ubus": {
                "session": [
                    "access",
                    "login"
                ]
            }
        }
    }
}
```

/usr/share/rpcd/acl.d/root.json:

```
{
        "root": {
                "description": "acl for root",
                "read": {
                        "ubus": {
                                "imgtrans": [],
                        },
                },
                "write": {
                        "ubus": {
                                "imgtrans": [ "*" ],
                        },
                }
        }
}
```

测试：

```
rpcd  &
uhttpd -u /ubus -p 0.0.0.0:80
(测试无鉴权场景，使用-a参数)
```

```


申请session
curl http://192.168.99.101/ubus -d '{ "jsonrpc": "2.0", "id": 1, "method": "call", "params": [ "00000000000000000000000000000000", "session", "login", { "username": "root", "password": ""  } ] }'
应答
{"jsonrpc":"2.0","id":1,"result":[0,{"ubus_rpc_session":"de7927ec55ff12e2ec9ed320838b0ae0","timeout":300,"expires":300,"acls":{},"data":{"username":"root"}}]}

尝试读imgtrans.vi
curl -s -d '{ "jsonrpc": "2.0", "id": 1, "method": "call", "params": [ "de7927ec55ff12e2ec9ed320838b0ae0", "imgtrans", "vi", {} ] }'  http://192.168.99.101/ubus
应答
{"jsonrpc":"2.0","id":1,"result":[0,{"online":false,"mode":"PAL","framerate":0,"width":0,"height":0}]}

list可用ubus项
curl -d '{"jsonrpc":"2.0","method":"list","params":["de7927ec55ff12e2ec9ed320838b0ae0","*"],"id":1}'  http://192.168.99.101/ubus
```

uhttpd:

https://openwrt.org/docs/guide-user/services/webserver/uhttpd

openwrt-rpcd服务ACL配置错误风险分析
https://www.secpulse.com/archives/71823.html

