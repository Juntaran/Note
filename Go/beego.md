# beego

在此记录一些 beego 的坑  

### 注解路由:

1. 注解路由 include 相应 controller 
2. 在 controller 的 method 方法上面加入注释 `// @router`  
3. bee run  

记得使用 `bee run` 来编译，`go build` 无法生成注解  
只有 `conf/app.conf` 的 `runmode` 为 `dev` 才可以  

