

---

## 提示缺少build-aux

```bash
dev@develop:~/workspaces/libnl$ autoreconf
configure.ac:51: error: required file 'build-aux/ar-lib' not found
configure.ac:51:   'automake --add-missing' can install 'ar-lib'
configure.ac:51: error: required file 'build-aux/compile' not found
configure.ac:51:   'automake --add-missing' can install 'compile'
configure.ac:73: error: required file 'build-aux/config.guess' not found
configure.ac:73:   'automake --add-missing' can install 'config.guess'
configure.ac:73: error: required file 'build-aux/config.sub' not found
configure.ac:73:   'automake --add-missing' can install 'config.sub'
configure.ac:49: error: required file 'build-aux/install-sh' not found
configure.ac:49:   'automake --add-missing' can install 'install-sh'
configure.ac:73: error: required file 'build-aux/ltmain.sh' not found
configure.ac:49: error: required file 'build-aux/missing' not found
configure.ac:49:   'automake --add-missing' can install 'missing'
lib/Makefile.am: error: required file 'build-aux/depcomp' not found
lib/Makefile.am:   'automake --add-missing' can install 'depcomp'
parallel-tests: error: required file 'build-aux/test-driver' not found
parallel-tests:   'automake --add-missing' can install 'test-driver'
```

解决方法：
```
automake --add-missing
autoreconf -i
```