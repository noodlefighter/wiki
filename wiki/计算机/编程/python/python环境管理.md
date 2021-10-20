## python 使用 Pipenv 管理环境

Pipenv = pyenv（管理python版本） + pip（管理依赖） + virtualenv（提供虚拟环境），整合起来，以获得良好的体验。

pip 是 Python 的包管理器；virtualenv 是虚拟环境，为你的创建虚拟的rootfs，为 shell 设置各种环境变量，可以在这个环境中用 pip 安装依赖；Pipfile 是 lock 文件，用于代替 requirements.txt。

https://pipenv.pypa.io/en/latest/

使用它的理由：

- 帮做了一些额外的事，比如工程级别指定源
- 和 pip 命令兼容，无学习成本的环境、依赖管理

安装：

```
$ pip install --user pipenv
或者安装时指定源
$ pipenv install --pypi-mirror https://mirrors.ustc.edu.cn/pypi/web/simple
```

项目使用：

```
$ cd project
$ pipenv install

直接在环境中运行命令
$ pipenv run python
或者可以让整个shell进入环境
$ pipenv shell
```

添加依赖，不应像 virtualenv 里直接用 pip 添加，而是用 pipenv 命令：

```
$ pipenv install requests
$ pipenv install requests~=1.2
$ pipenv install -r requirements.txt
```

关于 pipfile 和 pipfile.lock 的[建议](https://pipenv-fork.readthedocs.io/en/latest/basics.html)：

- Generally, keep both Pipfile and Pipfile.lock in version control.
- Do not keep Pipfile.lock in version control if multiple versions of Python are being targeted.
- Specify your target Python version in your Pipfile’s [requires] section. Ideally, you should only have one target Python version, as this is a deployment tool. python_version should be in the format X.Y and python_full_version should be in X.Y.Z format.

更多细节可以查看`pipenv --man`


> 博文参考：https://www.maxieewong.com/Pipenv.html

### 遇到的问题

`termios.error: (25, 'Inappropriate ioctl for device')`：不应该在 docker 环境中用`pipenv shell`

` Warning: Python 3.9 was not found on your system... Neither 'pyenv' nor 'asdf' could be found to install Python.`：可以安装 pyenv；或者，如果对python版本不敏感，可以将 Pipfile 中的 python 版本删掉，并将 Pipfile.lock 从版本管理中删除

Gitlab CI 中，只能缓存工程目录下面的文件，需要让 venv 在功能目录内：`export PIPENV_VENV_IN_PROJECT="enabled"`


## python 的 pyenv 管理多个 python 版本

安装，有[脚本](https://github.com/pyenv/pyenv-installer)：

```
$ curl https://pyenv.run | bash
$ echo 'export PATH=~/.pyenv/bin:$PATH' >> ~/.bashrc
```

脚本会使用 github 源，国内网络问题，没代理环境，想顺利使用可以换镜象，替换：

```
if [ -n "${USE_GIT_URI}" ]; then
  GITHUB="git://github.com.cnpmjs.org"
else
  GITHUB="https://github.com.cnpmjs.org"
fi
```





## python的virtualenv使用

> 已有更好的代替品 pipenv

安装：

```
$ pip3 install virtualenv
```

使用：

```
$ mkdir myproject
$ virtualvir ./myproject
$ cd myproject
$ source ./bin/active
```

在vscode中使用virtualenv环境：

1. 打开命令菜单（一般是Ctrl+Shift+P），输入`Python: Select Interpreter`
2. 找到由virtualenv创建的`bin/python`
3. 详情参考vscode的文档：[Using Python environments in VS Code](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter)



## python的venv使用

> 已有更好的代替品 pipenv
> 
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
```

