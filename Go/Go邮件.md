# Go 邮件

可能会遇到调用 `shell` 发送邮件标题包含中文发不出去的情况  


### 安装 sendmail  

``` bash
yum -y install sendmail
yum -y install mailx
service sendmail start Starting

# 测试
touch body.txt
echo 'This is test mail'>body.txt
mail -s 'Test mail' jacinthmail@gmail.com < body.txt

echo "This is test mail" | mail -s 'Test mail' juntaran@sina.com
```



使用 `base64` 编码  

> =?UTF-8?B?xxxxxx?=  

``` go
var subject = "测试test"
subject = "=?UTF-8?B?"+base64.StdEncoding.EncodeToString([]byte(subject))+"?="
```

___

## Reference 

* [linux shell发送邮件](http://littlewhite.us/archives/397)
