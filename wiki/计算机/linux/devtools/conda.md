

# anaconda

Conda是个包管理器，给科学计算领域提供环境。

## anaconda安装

https://docs.anaconda.com/anaconda/install/linux/

conda提供了一个shell脚本，向导式安装，实际上是给shell的启动脚本中插入布置conda环境的脚本段。

如果不希望用`conda init`安装，因为打开shell就会覆盖主机的环境，大多数时候会造成困扰，可以在`.bashrc`插入，只在键入`load-conda`时才载入conda环境：

```
load-conda()
{
       __conda_setup="$('/home/r/miniconda3/bin/conda' "shell.$(basename $SHELL)" 'hook' 2> /dev/null)"
       if [ $? -eq 0 ]; then
               eval "$__conda_setup"
       else
               if [ -f "/home/r/miniconda3/etc/profile.d/conda.sh" ]; then
                       . "/home/r/miniconda3/etc/profile.d/conda.sh"
               else
                       export PATH="/home/r/miniconda3/bin:$PATH"
               fi
       fi
       unset __conda_setup
}
```



## anaconda使用

`conda create`可以创建环境，例：

```
conda create -n myenv
conda create -n myenv python=3.8
```

`conda env`用于环境相关操作，比如列出所有已经创建的环境：

```
(base) ~ ᐅ conda env list
# conda environments:
#
base                  *  /home/r/miniconda3
TracKit                  /home/r/miniconda3/envs/TracKit
finger                   /home/r/miniconda3/envs/finger
math                     /home/r/miniconda3/envs/math
```

`conda activate`命令可以给当前shell切换环境：

```bash
~/proj/k210/TracKit $ conda activate TracKit
(TracKit) ~/proj/k210/TracKit $ python --version
Python 3.7.9
(TracKit) ~/proj/k210/TracKit $
```



## anaconda换源

清华源：https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/