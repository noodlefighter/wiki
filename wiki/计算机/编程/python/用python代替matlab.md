

一般用Matlab来做数据处理、科学计算、机器学习等，可以用SciPy替代，包含了算法库和数学工具包：

- NumPy：提供了数组，以及相关的大量数学函数
- Matplotlib：绘图库

>  参考：
>
>  numpy教程 https://www.runoob.com/numpy/numpy-tutorial.html
>
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





