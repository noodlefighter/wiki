---



> TODO: 

Golang适合快速开发，有GC不用自己管理内存，能优雅地和C/C++混编。但它的runtime似乎没实时性保证，因为垃圾回收机制可能会`Stop The World`，这里研究一下可行性。




https://github.com/rakyll/go-hardware

https://embd.kidoman.io/

https://qiita.com/tetsu_koba/items/7435ef8d0c77844d751e

https://studygolang.com/articles/11904

https://blog.csdn.net/qq_15427331/article/details/54613635

https://www.zhihu.com/question/21615032/answers/created

https://golang.org/doc/go1.10

https://blog.cloudflare.com/recycling-memory-buffers-in-go/

https://postd.cc/why-go-is-not-good/

http://blog.kmckk.com/archives/2712814.html

https://mender.io/blog/why-did-we-choose-golang-over-c

golang问题最大还是GC，即使不断优化，但还是用着老旧的算法，我们只能减少频繁创建对象，减轻GC的负担。

选用这种语言，很多时候是想利用他现成的库，如果那些库在设计的时候没这方面考量，那在嵌入式场合可能就不能直接拿来用（如果有go的嵌入式社区，可能又是另外一番景象了）