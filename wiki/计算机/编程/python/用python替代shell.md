

---



## 获取命令行参数

直接获取：

```
# $# 取参数数量
len(sys.argv)

# $0 取第0个参数
sys.argv[0]
```

使用`argparse`库:

```
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ssid', help='wlan ssid')
parser.add_argument('--sn', help='product serial number')
args = parser.parse_args()

print(args.ssid)
```

使用`click`库: https://click.palletsprojects.com/en/7.x/

```
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)

if __name__ == '__main__':
    hello()
```



## 像shell一样在字符串中插入变量

```
>>> a = 123
>>> print(f'a={a}')
a=123
```



## 路径操作

```
# 获取脚本所在路径
import os
script_dir = os.path.split(os.path.realpath(__file__))[0]
os.chdir(script_dir)

# 展开用户路径，方便跨平台
print(os.path.expanduser('~/.config'))
```



## 文件操作

```
# 检查文件是否存在
os.path.exists(file)

# rm -rf
os.system("rm -rf foo/")
shutil.rmtree("foo", ignore_errors=True)

# 打开文件读出每行内容
with open("./xxx.log") as file_obj:
	xxx_list = file_obj.read().splitlines()

# 遍历文件夹
g = os.walk(script_dir)

for path,dir_list,file_list in g:
    for dir in dir_list:
        print(os.path.join(path, file_name))

```



shutil模块可以代替很多shell的文件操作命令，可以避免特殊情况字符转义带来的困扰（比如括号，空格之类）：

```
import shutil

# 复制文件夹
shutil.copytree(src, dest) 

```





## 执行

```
# system命令同步执行命令，返回值为程序退出码
if os.system("echo abc") != 0:
	print("error: execute")
	exit(1)

# subprocess执行命令
import subprocess
res = subprocess.Popen('uptime', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
result = res.stdout.readlines()

# 例子，编译执行测试用例，当shell来用，check_call()会在执行返回错误时抛出错误
for test in tests:
	os.chdir(os.path.join(script_dir, test))
	output = subprocess.check_call(f"make", shell=True)
	output = subprocess.check_call(f"./test_case", shell=True)


# todo: 使用第三方sh模块 http://amoffat.github.io/sh/

```



## 使用glob匹配文件名

```
import glob
for name in glob.glob('dir/*'):
    print (name)
```

匹配表达式可以是：

- `'dir/*/*'`
- `'dir/*'`
- `'dir/file?.txt'`
- `'dir/*[0-9].*'`

