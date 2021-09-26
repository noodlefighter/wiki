## python 使用 Pipenv 管理依赖

Pipenv = pip + Pipfile + virtualenv，整合起来，以获得良好的体验。

pip 是 Python 的包管理器；virtualenv 是虚拟环境，为你的创建虚拟的rootfs，为 shell 设置各种环境变量，可以在这个环境中用 pip 安装依赖；Pipfile 是 lock 文件，用于代替 requirements.txt。

https://pipenv.pypa.io/en/latest/

使用 Pipenv 的项目：

```
$ cd project
$ pipenv install
$ pipenv shell
```

> 博文参考：https://www.maxieewong.com/Pipenv.html

## python的virtualenv使用

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



## python的venv使用[Invalid UTF-8]

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
```

