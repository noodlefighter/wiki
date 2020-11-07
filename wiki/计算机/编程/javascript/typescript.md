

## await关键字



例子（[来源](https://www.webhek.com/post/javascript-sleep-function.htm)）：

```
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

(async function() {
  console.log('Do some thing, ' + new Date());
  await sleep(3000);
  console.log('Do other things, ' + new Date());
})();
```

sleep函数立即返回了一个Promise对象，后面的程序立即得到执行了，为了实现阻塞，可以加await关键字。

