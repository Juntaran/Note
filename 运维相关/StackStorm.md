# StackStorm

*2017.8.5*

## 1. StackStorm 初步安装与测试

### 1.1 CentOS 7 安装 StackStorm

``` bash
sudo yum install curl nss
curl -sSL https://stackstorm.com/packages/install.sh | bash -s -- --user=st2admin --password='yourpassword'
```

设置防火墙规则  

``` bash
firewall-cmd --zone=public --add-service=http --add-service=https
firewall-cmd --zone=public --permanent --add-service=http --add-service=https
```

此时登录 `https://yourhost` ，输入设定的用户名和密码即可登录  

### 1.2 生成 token

``` bash
export ST2_AUTH_TOKEN=`st2 auth -t -p 'yourpassword' st2admin`
echo $ST2_AUTH_TOKEN
```

记下这个 token  

### 1.3 使用 st2 执行命令

#### 1.3.1 st2 使用 ssh 远程登录执行命令

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

#### 1.3.2 st2 本地执行命令

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

### 1.4 检查 st2 的 trigger

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

### 1.5 st2 的 rule 处理

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

### 1.6 官网示例

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


## 2. Action-Trigger-Rule

### 2.1 Action

#### 2.1.1 action 基础

action 可以理解为代码，可以使用任何语言编写  

可以使用以下命令来查看、运行 action  

``` bash
st2 action --h  # help 信息
st2 action list    # 列出所有 action
st2 action list -p linux    # 列出 linux 包的 action
st2 action get <action pack_name>   # 根据 action 的 pack 名来获取对应信息
st2 run <action> --h    # 列出该 action 的 help 信息
st2 run <action with parameters>   # 执行该 action
st2 action execute <action with parameters> # 执行该 action
st2 run linux.check_loadavg hosts='192.168.102.129' # 一个小例子
```

**这里有个坑，也就是 run 与 execute 的区别：**  

以 `core.http url="http://httpbin.org/get"` 这个 action 为例  

使用 `run` 会直接获取结果
``` bash
st2 run core.http url="http://httpbin.org/get"

# result:
id: 5986b5efe1382307a831a6b5
status: succeeded
parameters: 
  url: http://httpbin.org/get
result: 
  body:
    args: {}
    headers:
      Accept: '*/*'
      Accept-Encoding: gzip, deflate
      Connection: close
      Host: httpbin.org
      User-Agent: st2/v2.3.2
      X-Stanley-Action: http
    origin: 111.204.125.163
    url: http://httpbin.org/get
  headers:
    Access-Control-Allow-Credentials: 'true'
    Access-Control-Allow-Origin: '*'
    Connection: keep-alive
    Content-Length: '289'
    Content-Type: application/json
    Date: Sun, 06 Aug 2017 06:23:43 GMT
    Server: meinheld/0.6.1
    Via: 1.1 vegur
    X-Powered-By: Flask
    X-Processed-Time: '0.000948905944824'
  parsed: true
  status_code: 200
```

而使用 `action execute` 则会在后台执行，返回一个 id，如果想看结果还要再执行 `st2 execute get <id>`  

``` bash
# 执行第一步命令
st2 action execute core.http url="http://httpbin.org/get"

# 第一步的 result:
To get the results, execute:
 st2 execution get 5986b52de1382307a831a6b2

# 执行第二步命令
st2 execution get 5986b52de1382307a831a6b2

# 第二步的 result:
id: 5986b52de1382307a831a6b2
status: succeeded (3s elapsed)
parameters: 
  url: http://httpbin.org/get
result: 
  body:
    args: {}
    headers:
      Accept: '*/*'
      Accept-Encoding: gzip, deflate
      Connection: close
      Host: httpbin.org
      User-Agent: st2/v2.3.2
      X-Stanley-Action: http
    origin: 111.204.125.163
    url: http://httpbin.org/get
  headers:
    Access-Control-Allow-Credentials: 'true'
    Access-Control-Allow-Origin: '*'
    Connection: keep-alive
    Content-Length: '289'
    Content-Type: application/json
    Date: Sun, 06 Aug 2017 06:20:32 GMT
    Server: meinheld/0.6.1
    Via: 1.1 vegur
    X-Powered-By: Flask
    X-Processed-Time: '0.000990152359009'
  parsed: true
  status_code: 200
```

#### 2.1.2 action 的构成

一个 action 由两点构成：
> 1. 一个实现 action 逻辑的脚本  
> 2. 一个描述 action 的 yaml 文件  

脚本在退出时，状态为0表示成功，非0则表示失败，日志信息应该输出到标准错误  

yaml 元数据文件结构：

|  名称  |  说明  |
|----|----|
|  name  |  action 的名称  |
|  runner_type  |  该 action 的执行类型，例如 local-shell-cmd 、python-script 等，详见下表  |
|  enabled  |  能否被调用，一般填 true 就好  |
|  entry_point  |  该 action 对应的启动脚本路径下的名字，路径默认为 `/opt/stackstorm/packs/${pack_name}/actions/`  |
|  parameters  |  参数  |

|  runner_type  |  说明  |
|----|----|
|  local-shell-cmd  |  本地执行 shell 命令  |
|  local-shell-script  |  本地执行 shell 脚本  |
|  remote-shell-cmd  |  远程执行 shell 命令  |
|  remote-shell-script  |  远程执行 shell 脚本  |
|  python-script  |  python 脚本，action 由一个 python 类的 run() 方法执行  |
|  http-request  |  HTTP 客户端执行 HTTP 请求或运行 HTTP action  |
|  action-chain  |  执行简单的线性工作流(work flow)  |
|  mistral-v2  |  执行复杂的工作流(work flow)，建立于 Mistral OpenStack 之上  |
|  cloudslang  |  执行复杂的工作流(work flow)，建立于 CloudSlang 之上  |

官网 action yaml 例子：

``` yaml
---
name: "send_sms"
runner_type: "python-script"
description: "This sends an SMS using twilio."
enabled: true
entry_point: "send_sms.py"
parameters:
    from_number:
        type: "string"
        description: "Your twilio 'from' number in E.164 format. Example +14151234567."
        required: true
        position: 0
    to_number:
        type: "string"
        description: "Recipient number in E.164 format. Example +14151234567."
        required: true
        position: 1
        secret: true
    body:
        type: "string"
        description: "Body of the message."
        required: true
        position: 2
        default: "Hello {% if system.user %} {{ system.user }} {% else %} dude {% endif %}!"
```

yaml 文件解释：

该 action 使用 python 脚本执行，该 python 脚本为存放于同步录下的 `send_sms.py` 文件  
执行需要三个参数：`from_number`，`to_number`，`body`  
可以看到 body 参数具有默认值，to_number 的 `secret` 字段为 `true`  
如果一个属性被标记为 `secret` ，那么在 StackStorm 的日志中会隐藏它  

#### 2.1.3 action 的注册

一个 action 的注册有两个步骤：
> 1. 把它的文件放到目录里，/opt/stactstorm/packs   
> 2. 告诉系统哪个 action 可以使用  

一次性 action 可以放到 default 包里，/opt/stackstorm/packs/default/actions  

注册个人的 action 可以调用 `st2 action create mu_action_metadata.yaml` 命令  
如果需要重新加载所有 action，执行 `st2ctl reload --register-actions`  
全局重载可以执行 `st2ctl reload --register-all`  


#### 2.1.4 实现一个 remote-shell-script action

进入 example 包创建一个 action  

``` bash
cd /opt/stackstorm/packs/examples/actions
```

bash 脚本文件 remove_test.sh：  

``` bash
#!/usr/bin/env bash

ARGS=$1
FILE=$2
rm -${ARGS} ${FILE}
```

对应的 yaml 文件 remove_test.yaml：  

``` yaml
---
name: "remove_test"
runner_type: "remote-shell-script"
description: "remove a test file"
enabled: true
entry_point: "remove_test.sh"
parameters:
    args:
        type: "string"
        description: "args of rm"
        required: true
        position: 0
    file:
        type: "string"
        description: "File to remove"
        required: true
        position: 1
```

注册 remove_test 的 action  

``` bash
st2 action create remove_test.yaml
st2ctl reload --register-actions
```

在 VPN 服务器 138.128.206.71 的 `/root` 目录下创建一个测试文件 `test.c`  

执行该 action：  

``` bash
st2 run examples.remove_test hosts='138.128.206.71' port='27226' username='root' password='*****' args='rf' file='/root/test.c'
```

这里就相当于 ssh 连接到 138.128.206.71 的 27226 端口，使用 root 账户登录，执行了 `rm -rf /root/test.c` 命令  

#### 2.1.5 实现一个 python-script action

python 脚本文件 my_echo_action.py：  

``` python
import sys
from st2actions.runners.pythonrunner import Action

class MyEchoAction(Action):
    def run(self, message):
        print(message)
        if message == 'working':
            return (True, message)
        return (False, message)
```

对应的 yaml 文件 my_echo_action.yaml：  

``` yaml
---
name: "echo_action"
runner_type: "python-script"
description: "Print message to standard output."
enabled: true
entry_point: "my_echo_action.py"
parameters:
    message:
        type: "string"
        description: "Message to print."
        required: true
        position: 0
```

注册 my_echo_action 的 action  

``` bash
st2 action create my_echo_action.yaml
st2ctl reload --register-actions
```

测试结果：  

``` bash
st2 run examples.echo_action message='rua~'
.
id: 5986dbbfe1382307a831a6d3
status: failed
parameters: 
  message: rua~
result: 
  exit_code: 0
  result: rua~
  stderr: ''
  stdout: 'rua~'

st2 run examples.echo_action message='working'
..
id: 5986dbcbe1382307a831a6d6
status: succeeded
parameters: 
  message: working
result: 
  exit_code: 0
  result: working
  stderr: ''
  stdout: 'working'
```

### 2.2 Sensors 和 Trigger

`传感器(Sensor)` 的作用是把 `外部系统` 和 `事件` 与 `StackStorm` 结合起来  
传感器是使用 `Python` 写的，利用 `周期轮询检查外部系统` 或是 `被动地等待事件的发生`  
之后传感器连接 `触发器(Tirgger)` 到 `StackStorm` ，来匹配 `Rule` ，执行 `action`  

`触发器(Trigger)` 的作用是识别传入给 StackStorm 的事件  
一个触发器为 类型 (string) 和可选参数 (object) 的 tuple  
`Rule` 和 `Trigger` 共同工作  
传感器通常注册触发器，但是也有例外  
比如常用的 `webhooks` 触发器触发注册 StackStorm ，但是它不需要一个传感器  


_trigger & rule 没有太弄懂，待续_


## 3. ChatOps

一句话来说就是通过聊天软件如 slack 来控制 Ops  

> 关键文件 /opt/stackstorm/chatops/st2chatops.env  

根据选择的客户端，修改 `st2chatops.env`  

``` bash
export HUBOT_ADAPTER=slack
export HUBOT_SLACK_TOKEN=xoxb-*******
```

创建自定义的 pack  

``` bash
cd /opt/stackstorm/packs/
mkdir -p my-chatops/{actions,rules,sensors,aliases}
```

示例：  
在 `aliases` 文件夹中创建一个 action  
`aliases` 会通过 ssh 使用 `core.remote` 的 action 来执行命令  

创建一个 remote.yaml  

```yaml
# packs/my-chatops/aliases/remote.yaml
---
name: "remote_shell_cmd"
action_ref: "core.remote"
description: "Execute a command on a remote host via SSH."
formats:
  - "run {{cmd}} on {{hosts}}"
```

令该 action 生效：  

``` bash
sudo st2ctl reload --register-all
sudo service st2chatops restart
```

之后可以通过在机器人客户端执行 `!run <cmd> on <host>` 来在客户端查看命令执行的结果   
也可以执行 `<hubot name>, <cmd> on <host>` 来在客户端查看命令执行的结果  

多命令组合写法：  

``` bash
!run cd /root; tree -L 2 -d on '138.128.206.71' port='27226' username='root' password='******'
```

**这里的坑：**

> 1. 一些网络命令的问题，比如 ping，在客户端中输入 `!run ping baidu.com -c 3` 会报错，在网页控制台查看 history 会发现原因是默认把 `baidu.com` 转换成了 `http://baidu.com`，在网页控制台使用填参数的方法可以顺利执行，此问题经多次测试无解，此处在客户端只能 `ping ip`  
> 2. 一些命令不识别的问题，例如 `fdisk`、`ss`、`mpstat`、`ifconfig` 等会返回 `bash: fdisk: command not found` 的错误，而 `free`、`tree`、`netstat` 等就可以执行，这里的处理就需要写脚本文件了  

______

## Reference:
* [stackstorm](https://docs.stackstorm.com)