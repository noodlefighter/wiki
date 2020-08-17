

---



## 获取命令行参数

```
# $# 取参数数量
len(sys.argv)

# $1 取第一个参数
sys.argv[0]
```



```
parser = argparse.ArgumentParser()
parser.add_argument('--ssid', help='wlan ssid')
parser.add_argument('--sn', help='product serial number')
args = parser.parse_args()

print(args.ssid)
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

# todo: 使用第三方sh模块 http://amoffat.github.io/sh/

```



## 使用pexpect进行交互式操作