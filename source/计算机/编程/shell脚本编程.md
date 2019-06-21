

---



## 获取脚本所在目录

获取脚本所在路径, 而不是$PWD

```
SHELL_DIR=$(cd "$(dirname "$0")";pwd)
cd $SHELL_DIR
```

## 判断环境变量是否存在

```
if [ -z $JAVA_HOME ];then
	echo "not exists"
else
	echo "JAVA_HOME = $JAVA_HOME"
fi
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
[ STRING1 = STRING2 ] 如果两个字符串相同则为真 ；
[ STRING1 != STRING2 ] 如果字符串不相同则为真 ；
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