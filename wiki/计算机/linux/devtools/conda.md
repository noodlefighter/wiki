

# conda

Conda是个包管理器，给科学计算领域提供环境。

## conda安装

https://docs.anaconda.com/anaconda/install/linux/

conda提供了一个shell脚本，向导式安装，实际上是给shell的启动脚本中插入布置conda环境的脚本段。

## conda使用

`conda activate`命令可以给当前shell切换环境：

```bash
~/proj/k210/TracKit $ python --version
Python 3.8.3
~/proj/k210/TracKit $ conda activate TracKit
(TracKit) ~/proj/k210/TracKit $ python --version
Python 3.7.9
(TracKit) ~/proj/k210/TracKit $
```

