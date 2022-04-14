

## 给自己定的，写shell脚本时的原则

- 尽量不要写 shell 脚本，shell 脚本陷阱太多，写 shell 脚本前先问自己是否有必要，比如只是为了加载一些环境变量，否则不要写 shell 脚本
- 就算是简单的操作也要警惕，也尽量用 python 代替 shell 脚本，因为一开始简单的脚本可能在日后变成复杂的脚本
- 一定要从模板开始编写 shell 脚本，避免错误，比如如果没设``nounset`就可能出现类似`rm -rf $ABC/`但ABC变量不存在而删除根目录的情况

## shell 脚本模板

```
#!/bin/bash

set -o nounset
set -o errexit

SHELL_DIR=$(cd "$(dirname "$0")";pwd)

```

## 技巧

### 获取脚本所在目录

获取脚本所在路径, 而不是$PWD:

```
cd "$(dirname "$0")"
```



```
SHELL_DIR=$(cd "$(dirname "$0")";pwd)
```



当需要用source调用这个脚本时，上面这个`$0`是不可靠的，得换成`${BASH_SOURCE[0]}`：

https://stackoverflow.com/questions/35006457/choosing-between-0-and-bash-source


### 不显示所有stdout/stderr

```
$ do_something >/dev/null 2>&1
```

### 忽略错误

```
umount /aa/bb || true
```



### 判断环境变量是否存在

```
if [ -z $JAVA_HOME ];then
	echo "not exists"
else
	echo "JAVA_HOME = $JAVA_HOME"
fi
```

### 判断命令是否存在

```
function program_exists {
    hash "$1" 2> /dev/null
}

if program_exists python3; then
    PY=python3
elif program_exists python; then
    PY=python
    if [ $(python -c 'import sys; print(sys.version_info[:][0])') != '3' ]; then
        echo "python3 not found, will exit.."
        return 1
    fi
fi
```

### 查看进程是否存在

```
ps -fe|grep hostapd |grep -v grep
if [ $? -ne 0 ]; then
    echo "start process....."
else
    echo "runing....."
fi
```

### 判断文件是否相同

应该避免用diff命令，有性能问题，cmp命令会在发现第一个不同的

```
cmp --silent $old $new
```



### 随机选一个文件

```
ls |sort -R |tail -1
```



## 传参

```
$0 第0个参数(执行的命令本身)
$1 第1个参数
$2 第2个参数
$# 参数数量, "ps -a"有1个参数；"tar -xf aaa.tar"有2个参数
$? 上一条命令返回值
$* 所有参数
```

shift可以左移处理过的参数，比如以下脚本：

```
echo $*
shift 1
echo $*
```

输入`1 2 3`输出：

```
1 2 3
2 3
```



## 管道

0 STDIN 1 STDOUT 2 STDERR

```
> 输出到
& 后台运行, 如 echo abc &
|more和|less 用管道把上一条命令导过来显示，方便查看，比如一屏看不完的时候可以用上

用../source.txt批量覆盖找到的a.txt
find -name "a.txt"|xargs -I{} cp -f ../source.txt {}

|grep 根据关键词获取到某行内容
|awk 'NR==3 {print $1}' 获取第3行的第1个“参数”

将stderr重定向到stdout，stdout重定向到foo.log文件
cat foo > foo.log 2>&1

stdout不输出，将stderr重定向到stdout（可以用来收集日志）
ls 2iojedn 2>&1 1>/dev/null |grep ls
```

## xargs

stdin作为参数执行命令

```
-n 参数个数 -i 用{}替换参数
$ echo -e "1\n2\n3" |xargs -n 1 echo
$ echo -e "1\n2\n3" |xargs -n 1 -i echo {} line

```

## 获取命令的输出

```
方法1:
STR=`echo 123`
方法2:
STR="$(echo 123)"
```



## if语句

```
if [ 条件 ];then
   echo "do some thing"
elif [ 条件 ];then
   echo "do some thing"
else
   echo "do some thing"
fi
```

## for语句

```
# 遍历多行文本
my_multiline_str="a\
b\
c"
for line in $my_multiline_str;do
	echo "${line}"
done

# 遍历数组, 千万别写成了遍历多行文本的形式...血泪教训
my_array=(a b c)
for item in ${my_array[@]};do
	echo "${item}"
done

# 单行
while true; do echo hahaha;sleep 1; done
while true; do smartctl -x /dev/nvme1 |grep 'Temperature Sensor';sleep 60; done
```

## while语句

计算1到100的和

```bash
#!/bin/bash
i=1
sum=0
while [ $i -le 100 ]
do
  let sum=sum+$i
  let i++
done
echo $sum
```

死循环

```
while :
do
  echo ...
done
```



## case语句

```
case "$1" in
    start)        
        echo "start"
        ;;
    stop)
        echo "stop"
        ;;
    restart|reload)
        echo "restart"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac
```



## 拆分以空格分隔的字符串，比如参数

也可以用awk，但这样更快，注意下标从1开始：

```
arr=($(echo 1 2 3))
echo ${arr[1]}
echo ${arr[2]}
echo ${arr[3]}
```



## 遍历目录

```
for file in `ls $1`; do
	echo $1/file
done
```



## 文件判断

```
[ -b FILE ] 如果 FILE 存在且是一个块特殊文件则为真。
[ -c FILE ] 如果 FILE 存在且是一个字特殊文件则为真。
[ -d DIR ] 如果 FILE 存在且是一个目录则为真。
[ -e FILE ] 如果 FILE 存在则为真。
[ -f FILE ] 如果 FILE 存在且是一个普通文件则为真。
[ -g FILE ] 如果 FILE 存在且已经设置了SGID则为真。
[ -k FILE ] 如果 FILE 存在且已经设置了粘制位则为真。
[ -p FILE ] 如果 FILE 存在且是一个名字管道(F如果O)则为真。
[ -r FILE ] 如果 FILE 存在且是可读的则为真。
[ -s FILE ] 如果 FILE 存在且大小不为0则为真。
[ -t FD ] 如果文件描述符 FD 打开且指向一个终端则为真。
[ -u FILE ] 如果 FILE 存在且设置了SUID (set user ID)则为真。
[ -w FILE ] 如果 FILE存在且是可写的则为真。
[ -x FILE ] 如果 FILE 存在且是可执行的则为真。
[ -O FILE ] 如果 FILE 存在且属有效用户ID则为真。
[ -G FILE ] 如果 FILE 存在且属有效用户组则为真。
[ -L FILE ] 如果 FILE 存在且是一个符号连接则为真。
[ -N FILE ] 如果 FILE 存在 and has been mod如果ied since it was last read则为真。
[ -S FILE ] 如果 FILE 存在且是一个套接字则为真。
[ FILE1 -nt FILE2 ] 如果 FILE1 has been changed more recently than FILE2, or 如果 FILE1 exists and FILE2 does not则为真。
[ FILE1 -ot FILE2 ] 如果 FILE1 比 FILE2 要老, 或者 FILE2 存在且 FILE1 不存在则为真。
[ FILE1 -ef FILE2 ] 如果 FILE1 和 FILE2 指向相同的设备和节点号则为真。
```

## 字符串判断

```
[ -z STRING ] 如果STRING的长度为零则为真 ，即判断是否为空，空即是真；
[ -n STRING ] 如果STRING的长度非零则为真 ，即判断是否为非空，非空即是真；
[ STRING1 = STRING2 ] 如果两个字符串相同则为真，如[ "$USBMODE" == "host" ]
[ STRING1 != STRING2 ] 如果字符串不相同则为真，如[ "$USBMODE" != "host" ]
[ STRING1 ]　 如果字符串不为空则为真,与-n类似
```

## 数值判断

```
INT1 -eq INT2           INT1和INT2两数相等为真 ,=
INT1 -ne INT2           INT1和INT2两数不等为真 ,<>
INT1 -gt INT2            INT1大于INT1为真 ,>
INT1 -ge INT2           INT1大于等于INT2为真,>=
INT1 -lt INT2             INT1小于INT2为真 ,<</div>
INT1 -le INT2             INT1小于等于INT2为真,<=
```

## 复杂逻辑判断

```
-a 与
-o 或
! 非
```

例1:  如果a>b且a
```
if (( a > b )) && (( a < c ))
if [[ $a > $b ]] && [[ $a < $c ]]
if [ $a -gt $b -a $a -lt $c ]
```

例2:如果a>b或a
```
if (( a > b )) || (( a < c ))
if [[ $a > $b ]] || [[ $a < $c ]]
if [ $a -gt $b -o $a -lt $c ]
```

## 数组操作

```
# 创建数组
my_array=(value1 ... valueN)
# 赋值
my_array[0]=value0
my_array[1]=value1
# 取值
echo ${array_name[0]}

echo "数组的元素为: ${my_array[*]}"
echo "数组的元素为: ${my_array[@]}"
echo "数组元素个数为: ${#my_array[*]}"
echo "数组元素个数为: ${#my_array[@]}"

# 末尾追加元素
my_array+=(value)
my_array+=("${other_array[@]}")

# 遍历数组
for item in ${my_array[@]};do
	echo "${item}"
done
```

## 字符串操作

获取字符串长度

```
${#var}
```

字符串截取

```
# 最小限度从前面截取word(例a/b/c-->b/foo)
${var#*word}
# 最大限度从前面截取word(例a/b/c-->c)
${var##*word}

# 最小限度从后面截取word(例a/b/c-->a/b)
${var%word*}
# 最大限度从后面截取word(例a/b/c-->a)
${var%%word*}

# 从左边第start个字符，截取len个字符
${var:start:len}
${var:start}

# 从右边第start个字符，截取len个字符
${var:0-start:len}
${var:0-start}
```

## 异常捕获的一种方法

> via:https://stackoverflow.com/questions/22009364/is-there-a-try-catch-command-in-bash

利用`&&`短路性：

```sh
{ # try
    command1 &&
    command2 &&
    command3
} || { # catch
    echo “error catch”
}
```

感觉很容易漏写`&&`，特别是维护的人。

## 获取文件大小

```
wc -c _app.bin.enc | awk '{print $1}'
```

shell，bash，获取文件字节数

## 十六进制数字字符串，大端转小端

```
hex_string_to_le() {
  printf %s "$1" | dd conv=swab 2> /dev/null | rev
}

hex_string_to_le 01020304
```



## cut命令

例：

```
$ wpa_cli -i wlan0 list_networks
network id / ssid / bssid / flags
0	a-610377	any	
1	a-6102D2	any	
2	a-6102CD	any

$ wpa_cli -i wlan0 list_networks | tail -n +2 | cut -f -1
0
1
2
```



## IFS分隔符

用分隔符可以控制shell的行为：

```
IP=220.112.253.111
IFS="."
TMPIP=$(echo $IP)
IFS=" " # space
echo $TMPIP | read ip1 ip2 ip3 ip4
INVERT_IP=$ip4.$ip3.$ip2.$ip1
```

```
IFS='|'
text='a a a a|b b b b|c c c c'
for i in $text;do echo "i=$i";done
```

使用的时候得注意，要用`\n`作为分隔符时，得写作`IFS=$'\n'`，原因不明

## 格式控制

> via:<https://www.cnblogs.com/yaohong/archive/2018/05/31/9118928.html>

```
输出特效格式控制：
\033[0m  关闭所有属性  
\033[1m   设置高亮度  
\03[4m   下划线  
\033[5m   闪烁  
\033[7m   反显  
\033[8m   消隐  
\033[30m   --   \033[37m   设置前景色  
\033[40m   --   \033[47m   设置背景色


光标位置等的格式控制：
\033[nA  光标上移n行  
\03[nB   光标下移n行  
\033[nC   光标右移n行  
\033[nD   光标左移n行  
\033[y;xH设置光标位置  
\033[2J   清屏  
\033[K   清除从光标到行尾的内容  
\033[s   保存光标位置  
\033[u   恢复光标位置  
\033[?25l   隐藏光标  

\33[?25h   显示光标

整理：
    编码 颜色/动作
　　0   重新设置属性到缺省设置
　　1   设置粗体
　　2   设置一半亮度(模拟彩色显示器的颜色)
　　4   设置下划线(模拟彩色显示器的颜色)
　　5   设置闪烁
　　7   设置反向图象
　　22 设置一般密度
　　24 关闭下划线
　　25 关闭闪烁
　　27 关闭反向图象
　　30 设置黑色前景
　　31 设置红色前景
　　32 设置绿色前景
　　33 设置棕色前景
　　34 设置蓝色前景
　　35 设置紫色前景
　　36 设置青色前景
　　37 设置白色前景
　　38 在缺省的前景颜色上设置下划线
　　39 在缺省的前景颜色上关闭下划线
　　40 设置黑色背景
　　41 设置红色背景
　　42 设置绿色背景
　　43 设置棕色背景
　　44 设置蓝色背景
　　45 设置紫色背景
　　46 设置青色背景
　　47 设置白色背景
　　49 设置缺省黑色背景
特效可以叠加，需要使用“;”隔开，例如：闪烁+下划线+白底色+黑字为   \033[5;4;47;30m闪烁+下划线+白底色+黑字为\033[0m
下面是一段小例子

[plain] view plain copy
#!/bin/bash  
#  
#下面是字体输出颜色及终端格式控制  
#字体色范围：30-37  
echo -e "\033[30m 黑色字 \033[0m"  
echo -e "\033[31m 红色字 \033[0m"  
echo -e "\033[32m 绿色字 \033[0m"  
echo -e "\033[33m 黄色字 \033[0m"  
echo -e "\033[34m 蓝色字 \033[0m"  
echo -e "\033[35m 紫色字 \033[0m"  
echo -e "\033[36m 天蓝字 \033[0m"  
echo -e "\033[37m 白色字 \033[0m"  
#字背景颜色范围：40-47  
echo -e "\033[40;37m 黑底白字 \033[0m"  
echo -e "\033[41;30m 红底黑字 \033[0m"  
echo -e "\033[42;34m 绿底蓝字 \033[0m"  
echo -e "\033[43;34m 黄底蓝字 \033[0m"  
echo -e "\033[44;30m 蓝底黑字 \033[0m"  
echo -e "\033[45;30m 紫底黑字 \033[0m"  
echo -e "\033[46;30m 天蓝底黑字 \033[0m"  
echo -e "\033[47;34m 白底蓝字 \033[0m"  
  
#控制选项说明  
#\033[0m 关闭所有属性  
#\033[1m 设置高亮度  
#\033[4m 下划线  
echo -e "\033[4;31m 下划线红字 \033[0m"  
#闪烁  
echo -e "\033[5;34m 红字在闪烁 \033[0m"  
#反影  
echo -e "\033[8m 消隐 \033[0m "  
  
#\033[30m-\033[37m 设置前景色  
#\033[40m-\033[47m 设置背景色  
#\033[nA光标上移n行  
#\033[nB光标下移n行  
echo -e "\033[4A 光标上移4行 \033[0m"  
#\033[nC光标右移n行  
#\033[nD光标左移n行  
#\033[y;xH设置光标位置  
#\033[2J清屏  
#\033[K清除从光标到行尾的内容  
echo -e "\033[K 清除光标到行尾的内容 \033[0m"  
#\033[s 保存光标位置  
#\033[u 恢复光标位置  
#\033[?25| 隐藏光标  
#\033[?25h 显示光标  
echo -e "\033[?25l 隐藏光标 \033[0m"  
echo -e "\033[?25h 显示光标 \033[0m"  
```



## 技巧集

### 计算

取模：`echo 123 % 2 | bc`





### 获取CPU数

```
CPUS=$(cat /proc/cpuinfo |grep "processor"|wc -l)
```

已测试，在 git bash 和 msys2 环境中都可用，macos下用不了

也可以借助python：

```
CPUSecho "from multiprocessing import cpu_count\nprint(cpu_count())" | python
```



### 获取当前IP地址

```
ip="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
```

### 判断当前用户是否为root

```
#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi
```

### 像pip一样安装依赖Requirement.txt

```
cat packages.txt | xargs sudo apt-get -y install
```

### 取路径中的文件名和目录

```
MY_PATH=/tmp/abcd

# 取path中的文件名
echo $(basename $MY_PATH)
# 取path中的目录名
echo $(dirname $MY_PATH)
```

### 清屏

```
printf "\033c"
```

### 按行倒序读文件

读日志时有用：

```
$ tac file.txt | less
```



### 查找文件内容

> from: https://blog.csdn.net/JiaJunLee/article/details/50470643

```
从文件内容查找匹配指定字符串的行：
$ grep “被查找的字符串” 文件名
例子：在当前目录里第一级文件夹中寻找包含指定字符串的.in文件
grep “thermcontact” /.in

从文件内容查找与正则表达式匹配的行：
$ grep –e “正则表达式” 文件名

查找时不区分大小写：
$ grep –i “被查找的字符串” 文件名

查找匹配的行数：
$ grep -c “被查找的字符串” 文件名

从文件内容查找不匹配指定字符串的行：
$ grep –v “被查找的字符串” 文件名

从根目录开始查找所有扩展名为.log的文本文件，并找出包含”ERROR”的行
find / -type f -name “*.log” | xargs grep “ERROR”
例子：从当前目录开始查找所有扩展名为.in的文本文件，并找出包含”thermcontact”的行
find . -name “*.in” | xargs grep “thermcontact”
```

## 创建非阻塞的FIFO (no-blocking fifo)

FIFO默认行缓冲，导致一些应用场景下在异常时丢数据，比如记录日志的时候突然断电了，这时就想创建非阻塞的FIFO

参考爆栈回答：https://stackoverflow.com/questions/7360473/linux-non-blocking-fifo-on-demand-logging/7620387#7620387

用一个ftee小程序：

```
/* ftee - clone stdin to stdout and to a named pipe 
(c) racic@stackoverflow
WTFPL Licence */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <signal.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    int readfd, writefd;
    struct stat status;
    char *fifonam;
    char buffer[BUFSIZ];
    ssize_t bytes;
    
    signal(SIGPIPE, SIG_IGN);

    if(2!=argc)
    {
        printf("Usage:\n someprog 2>&1 | %s FIFO\n FIFO - path to a"
            " named pipe, required argument\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    fifonam = argv[1];

    readfd = open(fifonam, O_RDONLY | O_NONBLOCK);
    if(-1==readfd)
    {
        perror("ftee: readfd: open()");
        exit(EXIT_FAILURE);
    }

    if(-1==fstat(readfd, &status))
    {
        perror("ftee: fstat");
        close(readfd);
        exit(EXIT_FAILURE);
    }

    if(!S_ISFIFO(status.st_mode))
    {
        printf("ftee: %s in not a fifo!\n", fifonam);
        close(readfd);
        exit(EXIT_FAILURE);
    }

    writefd = open(fifonam, O_WRONLY | O_NONBLOCK);
    if(-1==writefd)
    {
        perror("ftee: writefd: open()");
        close(readfd);
        exit(EXIT_FAILURE);
    }

    close(readfd);

    while(1)
    {
        bytes = read(STDIN_FILENO, buffer, sizeof(buffer));
        if (bytes < 0 && errno == EINTR)
            continue;
        if (bytes <= 0)
            break;

        bytes = write(STDOUT_FILENO, buffer, bytes);
        if(-1==bytes)
            perror("ftee: writing to stdout");
        bytes = write(writefd, buffer, bytes);
        if(-1==bytes);//Ignoring the errors
    }
    close(writefd); 
    return(0);
}
```

测试：

```
$ ping www.google.com | ftee /tmp/mylog
$ cat /tmp/mylog
```
