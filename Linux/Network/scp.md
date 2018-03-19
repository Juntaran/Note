# scp

*2017.8.8*


公司神奇的网络设置，允许 `rz` ，不允许 `sz` ，不允许 `sftp`  
有 root 权限，还能连外网，真是无力吐槽  

公司分给了我一个开发服务器，只有我一个人用，却只能上传代码不能下载回来。。。  

这种情况下有两种解决方案：  

1. 使用 `nc` 监听端口传文件，恕我直言这样很蠢，而且传目录很费劲，在加上 windows 的 `nc` 苦不堪言  
2. 使用 `scp` 传到可用服务器，再从可用服务器 down 回来  

不用我说，看标题就知道选方案二了。。。  

从本地复制文件/文件夹到远程服务器：  
``` bash
# 传输文件
scp (-P remote_port) local_file (remote_username@)remote_ip:remote_folder/file 

# 传输文件夹
scp (-P remote_port) -r local_folder (remote_username@)remote_ip:remote_folder 
```

默认 scp 使用 `22` 端口，如果远程服务器修改了 ssh 端口，则需要加 `-P` 参数  
另外 `-P` 一定要紧跟 `scp` 后面  

不要忘记把可用服务器的文件删掉哦~~  

______

## Reference:
* [scp命令](http://www.cnblogs.com/hitwtx/archive/2011/11/16/2251254.html)