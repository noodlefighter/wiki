

## python单元测试框架pytest

> via: https://zhuanlan.zhihu.com/p/68088736

pytest会在当前路径下搜索`test_*.py`及`*_test.py`文件，并测试其中的`test_*`用例，如：

```
def inc(x):
    return x +1
 
def test_answer():
    assert inc(3) == 5
```

执行：

```
$ pytest
============================= test session starts=============================
collected 1 items
test_sample.py F
================================== FAILURES===================================
_________________________________ test_answer_________________________________
    def test_answer():
>       assert inc(3)== 5
E       assert 4 == 5
E        +  where 4 = inc(3)
 
test_sample.py:5: AssertionError
========================== 1 failed in 0.04 seconds===========================
```

