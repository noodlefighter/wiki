

## 使用pkg打包nodejs

`package.json`例子:

```
{
  "name": "wsubus-logread",
  "dependencies": {
    "ubus-websocket-communicator": "https://github.com/noodlefighter/ubus-websocket-communicator.git"
  },

  "bin": "wsubus-logread.js",
  "pkg": {
    "targets": [
      "node14-linux-x64",
      "node14-win-x64"
    ]
  }
}

```

打包：

```
$ sudo yarn global add pkg
$ pkg .
$ 7z a wsubus-logread-linux.7z wsubus-logread-linux
$ 7z a wsubus-logread-win.7z wsubus-logread-win.exe
```

