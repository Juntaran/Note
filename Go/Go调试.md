# Go 调试

## web 服务调试

go 中提供了 `pprof` 包来做代码的性能监控  

> net/http/pprof  
> runtime/pprof  

其实 `net/http/pprof` 中只是使用 `runtime/pprof` 包来进行封装了一下，并在 http 端口上暴露出来  

```go

package main

import (
	"github.com/astaxie/beego"
	_ "net/http/pprof"
	"net/http"
)

func main() {
	go http.ListenAndServe(":8080",nil)
	beego.Run()
}

```

之后登录 `http://localhost:8080/debug/pprof/` 即可查看  

`go tool pprof http://localhost:8080/debug/pprof/profile`  


## 应用服务调试

代码加入 `StartCPUProfile` 和 `StopCPUProfile`  

``` go

var cpuprofile = flag.String("cpuprofile", "", "write cpu profile to file")

func main() {
    flag.Parse()
    if *cpuprofile != "" {
        f, err := os.Create(*cpuprofile)
        if err != nil {
            log.Fatal(err)
        }
        pprof.StartCPUProfile(f)
        defer pprof.StopCPUProfile()
    }
}
```


运行时增加参数  
例如: `fabonacci --cpuprofile=fabonacci.prof`  

`go tool pprof fabonacci.prof`



## Reference

* [Go 的 pprof 使用](https://www.cnblogs.com/yjf512/archive/2012/12/27/2835331.html)
