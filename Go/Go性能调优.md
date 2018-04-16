# Go 性能调优

之前写的 [KafkaToDruid](https://github.com/Juntaran/Go_In_Action/tree/master/Demo/KafkaToDruid) 存在性能瓶颈  
为了进行性能优化，必须找出瓶颈，根据 [Go 调试](https://github.com/Juntaran/Note/blob/master/Go/Go%E8%B0%83%E8%AF%95.md) 这篇以前的笔记进行了进一步的深入  

1. 安装工具  

``` sh
brew install graphviz
go get github.com/uber/go-torch
git clone git@github.com:brendangregg/FlameGraph.git
cp FlameGraph/flamegraph.pl /usr/local/bin
cp $GOPATH/bin/go-torch /usr/local/bin
```

2. 修改代码的 `main` 函数  

``` go
import (
    _ "net/http/pprof"
    "runtime/pprof"
    "time"
    "flag"
)

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
    
    // 加入你的代码
    // 最好使用 go run()
    // 从而只使用一个定时器就能定时终结任务
    // 因为主 goroutine 终结之后其余 goroutine 也直接退出

    time.Sleep(time.Second * 20)
}
```

> 注意: 不能使用 `kill` 方式来终止，否则会记录为空

3. 开始记录  

``` sh
# 编译
go build main.go

# 记录
./main --cpuprofile=test.prof

# 使用 pprof
go tool main test.prof
```

可以输入 `web/pdf` 来生成文件，`web命令` 生成的 `svg` 在 `/tmp` 下，`pdf命令` 生成的 `pdf` 在当前目录  

4. 使用 `go-torch` 根据 `prof 文件` 生成火焰图  

``` bash
go-torch -b test.prof -f test_flame.svg
```

5. 观察 svg 图  

 
![svg_1](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_pprof_1.svg?sanitize=true)  
最初的 [svg 图](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_pprof_1.svg?sanitize=true) ，性能极差  

![flame_1](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_flame_1.svg)  
最初的 [火焰图](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_flame_1.svg) ，可以看出 `producer` 占用了很多时间  

![svg_2](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_pprof_2.svg?sanitize=true)  
第一次优化后的 [svg 图](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_pprof_2.svg?sanitize=true)  

![flame_2](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_flame_2.svg?sanitize=true)  
第一次优化后的 [火焰图](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_flame_2.svg?sanitize=true) ，可以看到 `gc` 占用了绝大部分  

![svg_3](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_pprof_3.svg?sanitize=true)  
去除了 `fmt.Println()` 并修改了字符串拼接，选择了 `bytes.Buffer` 后的 [svg 图](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_pprof_3.svg?sanitize=true)  

![flame_3](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_flame_3.svg?sanitize=true)  
最终优化后的 [火焰图](https://rawgit.com/Juntaran/Go_In_Action/master/Demo/KafkaToDruid/testing/k2d_flame_3.svg?sanitize=true)    


