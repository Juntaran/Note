# pycurl

pycurl.Curl()类实现创建一个libcurl包的Crul句柄对象，无参数  
Curl对象有以下几个常用的方法  

> close()方法，对应`libcurl`包中的`curl_easy_cleanup`方法，无参数，实现关闭、回收Curl对象
> perform()方法，对应`libcurl`包中的`curl_easy_perform`方法，无参数，实现Curl对象请求的提交
> setopt(option, value)方法，对应`libcurl`包中的`curl_easy_setopt`方法，参数`option`为通过libcurl常量来指定的，参数`value`值会依赖`option`
> getinfo(option)方法，对应libcurl`包中的`curl_easy_getinfo`方法，参数`option`通过`libcurl`常量指定