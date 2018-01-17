# http.NewRequest 的坑

http.NewRequest 传值深坑  

``` go
package main
import (
    "fmt"
    "io/ioutil"
    "net/http"
    "net/url"
    "strings"
)

func main() {
    v := url.Values{}
    v.Set("username", "xxxx")
    v.Set("password", "xxxx")
    // 利用指定的 method, url 以及可选的 body 返回一个新的请求.如果 body 参数实现了 io.Closer 接口，Request 返回值的 Body 字段会被设置为 body，并会被 Client 类型的 Do、Post 和 PostFOrm 方法以及 Transport.RoundTrip 方法关闭。
    body := ioutil.NopCloser(strings.NewReader(v.Encode())) //把form数据编下码
    client := &http.Client{}//客户端,被Get,Head以及Post使用
    reqest, err := http.NewRequest("POST", "http://xxx.com/logindo", body)
    if err != nil {
        fmt.Println("Fatal error ", err.Error())
    }
    // 给一个key设定为响应的value.
    reqest.Header.Set("Content-Type", "application/x-www-form-urlencoded;param=value") // 必须设定该参数,POST 参数才能正常提交

    resp, err := client.Do(reqest)//发送请求
    defer resp.Body.Close()//一定要关闭resp.Body
    content, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println("Fatal error ", err.Error())
    }

    fmt.Println(string(content))
}
```

注意 `Body` 是一个 `ReadCloser` 所以用 `NopCloser` 来转化 `Reader` 对象  
另外  

``` go
reqest.Header.Set("Content-Type", "application/x-www-form-urlencoded;param=value")
```

这句一定要带，不然不能提交  

___

## Reference

* [Golang 学习室](https://www.kancloud.cn/digest/batu-go/153529)
* [Golang Http Client 使用 Request 带参数进行Post请求](https://www.nichijou.com/p/n3jtw/)