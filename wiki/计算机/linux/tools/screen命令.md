

## screen命令保持会话

> screen 会话命令可以保持本地和服务器断开后，程序继续在服务器上运行，并且运行结束后，输出最后的结果。 功能结果相当于 nohup command &，但是功能远比nohup强大

用法：

```
创建/恢复会话
$ screen -R ABC
列出所有会话
$ screen -list
```

