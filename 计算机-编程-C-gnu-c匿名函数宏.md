title: gnu-c匿名函数宏
date: 2019-06-09
categories:
- 计算机
- 编程
- C


---

参考：

<https://gcc.gnu.org/onlinedocs/gcc/Statement-Exprs.html>

<https://gcc.gnu.org/onlinedocs/gcc/Nested-Functions.html>

## C语言实现匿名函数

> via: <https://www.cnblogs.com/eben-yl/p/4662567.html>

在C语言中可以通过宏定义的方式实现匿名函数,具体如下:

```c
`#define lambda(return_type, function_body) \``({ \``      ``return_type $``this` `function_body \``          ``$``this``; \``})``#define $ lambda`
```

该定义利用了GCC对C语言的扩展(被一对花括号包起来的代码块能够返回一个值),该宏定义能够返回$this(函数指针),如果我们需要一个返回两整数的和的函数,那么我们还可以对该宏再做一次封装,如下:

```c
`#define add2int(function_body) $(int, (int _a, int _b){function_body})`
```

然后我们就可以像下面这样来使用该宏(求一个整型数组所有元素的和):

```c
`int` `sum(``int` `*arr, ``int` `length, ``int` `(*add)(``int``, ``int``));``int` `main(``int` `argc, ``char` `**argv)``{``    ``int` `arr[] = { [0 ... 9] = 1, [10 ... 89] = 2, [90 ... 99] = 3 };``    ``int` `ret = sum(arr, ``sizeof``(arr)/``sizeof``(``int``), add2int(``int` `c = _a + _b; ``return` `c;));``    ``//add2int返回一个求两个整数和的函数` `    ``printf``(``"sum of arr is %d\n"``, ret);``}``int` `sum(``int` `*arr, ``int` `length, ``int` `(*add)(``int``, ``int``))``{``    ``int` `sum = 0;``    ``for` `(``int` `i=0; i < length; i++)``    ``{``        ``sum = add(sum, arr[i]);``    ``}``    ``return` `sum;``}`
```

当然也可以直接使用lambda宏,注意function_body需要包含函数的返回类型及参数列表,将上面第6行代码替换为:

```c
`int` `ret = sum(arr, ``sizeof``(arr)/``sizeof``(``int``), $(``int``, (``int` `_a, ``int` `_b){``    ``int` `c = _a + _b;``    ``return` `c;``});`
```

## 使用GCC语句表达式的匿名函数