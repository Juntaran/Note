# SSH隧道

*2017.7.20*


> SSH 隧道就是利用 SSH 进行端口转发，从而实现流往某端口的数据被加密后传向另一机器,
> 这个过程形似构造了一条通道，因此也称之为 SSH 隧道(SSH Tunnel)

## SSH 隧道的类型

1. 动态端口转发(socks 代理)
2. 本地端口转发
3. 远程端口转发

______

## 动态端口转发

- 条件:

> host1 ---ssh---> host2

- 目的：

> 让 host1 某端口的数据发往 host2，host2 根据其应用程序协议发出到指定地址，就好像是从 host2 直接发出的数据

- 操作：

1.在 host1 上执行以下命令

```
    ssh -D 127.0.0.1:7070 user@host2
```

2.设置代理  


- 验证：

```
    curl --socks5 localhost:7070 download-link
```
______

## 本地端口转发

- 条件:

> host1 <---> host2  
> host3 <---> host2  
> host1 <-x-> host3  

- 目的：

> 借助 host2 实现 host1 和 host3 的通信

- 操作：

1.在 host1 上执行以下命令

``` bash
    ssh -L 8080:host3:80 user@host2
    # 执行完成，在 host1 浏览器中 输入 localhost:8080 即可看到 host3 的 Web 页面 
    # 如果使用 xshell 等工具访问 host1, 那么可以使用 curl localhost:8080 来查看 Web 内容

```

2.在 host1 使用 ssh 登录 host3

``` bash
    ssh -L 2030:host3:22 user@host2
    # 现在可以在另开一个 host1 终端输入 : ssh -p 2030 user@host3 去登录 host3
```
______

## 远程端口转发

- 条件：

> host1 <-x-> host3  
> host2 <---> host3  
> host2 -ssh-> host1  
> host1 --x--> host2  
> 在这种条件下， host1 就不可以 ssh 连接 host2 了，所以不能使用`本地转发端口`了

- 目的：

> host2 可以 ssh 连接 host1, 那么 host1 就可以借助这条连接与 host3 进行通信

- 操作：

1.在 host2 上执行以下命令

``` bash
    # 通过访问 host1 本地 8080 端口来访问 host3 的 80 端口
    ssh -R 8080:host3:80 user@host1
    # 执行完成，在 host1 浏览器中 输入 localhost:8080 即可看到 host3 的 Web 页面
```

2.在 host2 上执行以下命令

```
    ssh -R 2030:host3:22 user@host1
```

3.host1 使用 ssh 登录 host3

```
    ssh -p 2030 user@host3
```
______

## SSH 一些辅助参数

| 参数  | 作用  |
|---|---|
| -q  | 安静模式. 抑制警告和诊断信息  |
| -T  | 不分配伪终端，只是使用隧道  |
| -N  | 不运行远程命令(仅对端口转发有用)  |
| -f  | 后台运行，配合 `-N` 一起使用，或者在命令结尾添加 `sleep 30`  |
| -n  | 重定向标准输入到 /dev/null(阻止从标准输入读)  |
| -o ServerAliveInterval=60  | 让 SSH 每隔一段时间发送一些消息，避免隧道关闭  |
| -v  | 打印调试信息  |

``` bash
    ssh -qTfnN -D 7070 xxx@yyy.com	# ssh 后台动态端口转发
```

______

## 列出 SSH 隧道脚本

``` bash
    ps -ef | grep ssh | awk '$3 == 1' | awk '{for (i=8;i<=NF;i++) printf $i""FS;print""}'
    # 结果
    ssh -f -N -p 2222 -R 1111:10.123.123.123:3333 10.234.234.234
    ssh -f -N -p 2222 -R 8080:10.123.123.123:8080 10.234.234.234
```

______

## 保持长时间连接

有些路由器会把长时间没有通信的连接断开。SSH 客户端的 `TCPKeepAlive` 选项可以避免这个问题的发生，默认情况下它是被开启的  
如果它被关闭了，可以在 ssh 的命令上加上 `-o TCPKeepAlive=yes` 来开启  
另外可以添加 `-o ServerAliveInterval=15` 

TCPKeepAlive 和 ServerAliveInterval 的区别在于

> ServerAliveInterval 是被加密过的，TCPKeepAlive 无法证实它是否是假冒的  



另一种方法是，去掉 `-N` 参数，加入一个定期能产生输出的命令  
例如: top 或者 vmstat 
``` bash
    ssh -f -p 2222 -R 1111:10.123.123.123:3333 10.234.234.234 vmstat 30 
```


______

## Reference:
* [倘若微小](http://www.ifmicro.com/%E8%AE%B0%E5%BD%95/2015/09/25/ssh-port-forwarding/)
* [serverfault](https://serverfault.com/questions/538897/serveralivecountmax-in-ssh/538919#538919)
* [SSH隧道自动检测脚本](http://chembo.iteye.com/blog/1926312)
* [SSH隧道与端口转发及内网穿透](http://blog.creke.net/722.html)
