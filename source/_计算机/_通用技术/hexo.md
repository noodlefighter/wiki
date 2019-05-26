

---



## Hexo 的 Template render error 错误

> via:<https://52heartz.top/articles/hexo-template-render-error/>
>
> 作者: [52Heartz](https://52heartz.top/)

原因可能有如下两种:

1. {% raw %}在 `.md` 源文件中出现了没有闭合的双括号，如单独的 `{{` 或者单独的 `}}`，或者出现了闭合的但是中间为空的双括号，如 `{{}}` 。{% endraw %}
2. {% raw %}在 `.md` 源文件中出现了没有闭合的标签插件（Tag Plugins）。如只有 `{% xxx %}`，但却没有 `{% endxxx %}`。{% endraw %}

{% raw %}更深层的原因是， {{ 和 }} ，以及 {% %} 是 Hexo 模板中的标签，Hexo 处理源文件的时候会对这些标签进行解析，但是单独写的或者使用不支持的标签就会导致解析错误。{% endraw %}

如果确实需要在文章中呈现出双括号或者括号加百分号这样的文字，可以直接在源文件中使用

```
{% raw %}
```



和

```
{% endraw %}
```