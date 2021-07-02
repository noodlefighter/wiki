

一般用Matlab来做数据处理、科学计算、机器学习等，可以用SciPy替代，包含了算法库和数学工具包：

- NumPy：提供了数组，以及相关的大量数学函数
- Matplotlib：绘图库

>  参考：
>
>  numpy教程 https://www.runoob.com/numpy/numpy-tutorial.html
>
>  SciPy Lecture Notes 中文版 https://wizardforcel.gitbooks.io/scipy-lecture-notes/content/index.html

> 文档：
> Numpy API： https://numpy.org/doc/stable/reference/
>  Matplotlib API：https://matplotlib.org/stable/api/index.html



## 环境布置：anaconda + vscode + jupyter

//TODO:



## 实例

创建环境：

```
$ conda create -n math python=3.8
$ conda activate math
$ pip install matplotlib
```

测试程序：

```
import numpy as np
import matplotlib.pyplot as plt

scale_val = 256
sample_rate = 16000
sin_freq = 10
half_scale = scale_val/2

x = np.arange(0, 16000)
y = half_scale * np.sin(x*sin_freq*(2*np.pi)/sample_rate) + half_scale
plt.plot(x, y)
plt.show()
```

## SymPy符号计算

数值计算和符号计算的区别，符号计算在过程中会保留符号，例如计算`sin(pi)`时，数值计算不保证结果为0，而符号计算最后计算得出0.

> 参考：
>
> - [SymPy符号计算-让Python帮我们推公式](https://zhuanlan.zhihu.com/p/83822118)
> - [SymPy 符号计算基本教程](https://zhuanlan.zhihu.com/p/111573239)

用SymPy可以帮助展开公式、化简数式.. 比如：

```
>>> x = symbols('x')
>>> simplify(sin(x)**2)
sin(x)**2
>>> simplify(sin(x)**2+cos(x)**2)
1
>>> simplify(sin(x)**2+cos(x)**2+x)
x + 1
```

带符号的矩阵计算例子：

```
>>> a = Matrix([[1, x], [3, 4], [0, 2]])
>>> b = Matrix([[3], [4]])
>>> a*b
Matrix([
[4*x + 3],
[     25],
[      8]])
```



## python音频合成

https://pythonaudiosynthesisbasics.com/

这个网站提示了

- 把声卡当信号发生器
- 生成正波形文件



