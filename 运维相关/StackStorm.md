# StackStorm

*2017.8.5*

## CentOS7 安装 StackStorm

``` bash
sudo yum install curl nss
curl -sSL https://stackstorm.com/packages/install.sh | bash -s -- --user=st2admin --password='yourpassword'
```

此时登录 `https://yourhost` ，输入设定的用户名和密码即可登录  

## 生成 token

``` bash
export ST2_AUTH_TOKEN=`st2 auth -t -p 'root' yourpassword`
echo $ST2_AUTH_TOKEN
```

记下这个 token  

## 使用 st2 执行命令

### st2 使用 ssh 远程登录执行命令

本部分已本地搭建的 stackstorm 环境连接租用的美国服务器 138.128.206.71 为例   

st2 使用 ssh 远程连接到另一个 `ip/hostname` 可以指定`端口、用户名、密码`  默认会进入 `/tmp` 目录  

``` bash
st2 run core.remote hosts='138.128.206.71' port='27226' username='root' password='*****' -- ls -l
```

如果想进入另一个目录执行命令  

``` bash
st2 run core.remote hosts='138.128.206.71' port='27226' username='root' password='*****' -- cd /root;ls -ltr
```

上一种方法在 web 界面只会看到执行了 `cd /root` 可以采用以下命令解决该问题

``` bash
st2 run core.remote hosts='138.128.206.71' port='27226' username='root' password='*****' cmd="cd /root; ls -ltr"
```

### st2 本地执行命令

本地执行命令和远程执行命令类似，有两种方法  

``` bash
st2 run core.local cmd="ls -al"
st2 run core.local -- ls -al
```

列出执行的任务  

``` bash
st2 execution list
```

根据任务 ID 获取结果  

``` bash
st2 execution get <execution_id>
```

获取最近的5个任务  

``` bash
st2 execution list -n 5
```

## 检查 st2 的 trigger

列出所有可用的触发器  

``` bash
st2 trigger list
```

检查间隔时间定时器触发细节

``` bash
st2 trigger get core.st2.IntervalTimer
```

检查 web 端的触发器细节

``` bash
st2 trigger get core.st2.webhook
```

## st2 的 rule 处理

创建一个 rule  

``` bash
st2 rule create /usr/share/doc/st2/examples/rules/sample_rule_with_webhook.yaml
```

列出所有 rule  

``` bash
st2 rule list
```

列出 example 包的所有 rule  

``` bash
st2 rule list --pack=examples
```

获取 examples.sample_rule_with_webhook 的 rule  

``` bash
st2 rule get examples.sample_rule_with_webhook
```

## 官网示例

``` bash
# Post to the webhook
curl -k https://localhost/api/v1/webhooks/sample -d '{"foo": "bar", "name": "st2"}' -H 'Content-Type: application/json' -H 'X-Auth-Token: yourToken'

# Check if the action got executed (this shows last action)
st2 execution list -n 1

# Check that the rule worked. By default, st2 runs as the stanley user.
sudo tail /home/stanley/st2.webhook_sample.out

# And for fun, same post with st2
st2 run core.http method=POST body='{"you": "too", "name": "st2"}' url=https://localhost/api/v1/webhooks/sample headers='x-auth-token=yourToken,content-type=application/json' verify_ssl_cert=False

# And for even more fun, using basic authentication over https
st2 run core.http url=https://httpbin.org/basic-auth/st2/pwd username=st2 password=pwd

# Check that the rule worked. By default, st2 runs as the stanley user.
sudo tail /home/stanley/st2.webhook_sample.out
```

复制 doc 的例子去运行

``` bash
# 复制 demo 到 packs
sudo cp -r /usr/share/doc/st2/examples/ /opt/stackstorm/packs/

# 执行 setup
st2 run packs.setup_virtualenv packs=examples

# 重新加载 stackstorm
st2ctl reload --register-all
```


______

Reference:
* [stackstorm](https://docs.stackstorm.com/install/index.html)