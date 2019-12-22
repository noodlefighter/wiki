title: selenium
date: 2019-08-25
categories:
- 计算机
- 前端技术
- tools




---

selenium是个浏览器自动化工具，操作例如Chrome的headless模式、PhantomJS（本身就是headless的，已停止开发）等浏览器。



github: https://github.com/SeleniumHQ/selenium

docs: https://seleniumhq.github.io/docs/index.html



## Selenium使用Headless Chrome浏览器

> via: https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug

```
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # # Bypass OS security model
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options)
print ("Headless Chrome Initialized on Linux OS")
```

还有建议用chromedriver的，在生产环境该用它吧。



## 使用Python+Selenium对某元素截图

> via: https://www.jianshu.com/p/7ed519854be7



```
from selenium import webdriver
from PIL import Image

driver = webdriver.Chrome()
driver.get('http://stackoverflow.com/')
driver.save_screenshot('screenshot.png')

left = element.location['x']
top = element.location['y']
right = element.location['x'] + element.size['width']
bottom = element.location['y'] + element.size['height']

im = Image.open('screenshot.png') 
im = im.crop((left, top, right, bottom))
im.save('screenshot.png')
```



## Selenium使用cookies



```
brower.add_cookie({
    "domain":".taobao.com",
    "name":"xxx",
    "value":"xxx",
    "path":'/',
    "expires":None
})
```

