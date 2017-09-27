# SSH 免密登陆

*2017.6.18*

从 A 机器的 a 账号 建立到 B 机器的 b 账号的 ssh 免密登陆  
以 ubuntu 虚拟机`juntaran`账号连接自己的 VPN 服务器`root`账号为例

    ssh root@138.128.206.71 -p 27226
    
此时需要输入密码

## 免密制作流程：

1. 为`juntaran`账号建立自己的公钥私钥，会在`/home/a/.ssh`中多出`id_rsa`和`id_rsa.pub`，分别是`私钥`和`公钥`

```
        ssh-keygen -t rsa
```
        
    全部回车跳过
        
2. 建立信任关系，默认端口号为22，如果需要修改端口则需要加上`-p`

```
        ssh-copy-id root@138.128.206.71 -p 27226
```
        
    旧版本可能不支持`-p`选项，可以采取以下措施
        
```
        ssh-copy-id "-p 27226 root@138.128.206.71"
```
        
    之后流程就很简单
    
```
        Are you sure you want to continue connecting (yes/no)? yes
```
        
    再输入密码即可
    
3. 直接免密登陆

```
        ssh root@138.128.206.71 -p 27226
```

## 免密简洁方案：

源 `/root/.ssh/id_rsa.pub` 内容，粘贴到目的机 `/root/.ssh/authorized_keys` 里