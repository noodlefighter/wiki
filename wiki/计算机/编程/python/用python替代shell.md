

---



## 获取命令行参数

```
# $# 取参数数量
len(sys.argv)

# $1 取第一个参数
sys.argv[0]
```



## 路径操作

```
# cd
os.chdir()

# 获取脚本所在路径
py_script_dir = os.path.split(os.path.realpath(__file__))[0]
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

```



## 执行

```
# system命令同步执行命令，返回值为程序退出码
if os.system("echo abc") != 0:
	print("error: execute")
	exit(1)

# todo: subprocess执行命令

# todo: 使用第三方sh模块 http://amoffat.github.io/sh/

```



## 使用pexpect进行交互式操作