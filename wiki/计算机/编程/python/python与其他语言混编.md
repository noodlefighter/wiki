

## python与c/cpp混编

可选方案：

- [ctypes](http://docs.python.org/library/ctypes.html)：python官方提供的方式，导入动态库
- [CFFI](https://github.com/Jairoguo/CFFI-Docs-ZH-CN)：优势是只需要知道C和Python，足够简单；提供ABI/API模式，官方建议用API模式
- [SWIG](https://github.com/noodlefighter/python-swig-c-test)：优势是适合把C API接口包装成其他各种语言的API，只需要维护一套中间代码
- [cppyy](https://cppyy.readthedocs.io/en/latest/)： Automatic Python-C++ bindings

用python或许可以给c做单元测试，比如：

- [用Python做C函数的单元测试](https://www.pynote.net/archives/2923)