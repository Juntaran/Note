# DNS处理：dnspython

dnspython提供了一个DNS解析器类——`resolver`，  
使用它的`query`方法来实现域名的查询功能  

    query(self, qname, rdtype=1, rdclass=1, tcp=False, source=None, raise_on_no_answer=True, source_port=0)

其中，`qname`参数为查询的域名，  
`rdtype`参数用来指定RR资源的类型，通常有以下几种  

> A记录：主机名转换为IP地址  
> MX记录：邮件交换记录，定义邮件服务器域名  
> CNAME记录：指别名记录，实现域名间的映射  
> NS记录：标记区域的域名服务器及授权子域  
> PTR记录：反向解析，与A记录相反，将IP转换为主机名  
> SOA记录：SOA标记，一个起始授权区的定义

`rdclass`参数用于指定网络类型，默认为IN，可选还有CH、HS  
`tcp`参数用于指定查询是否开启TCP协议，默认False  
`source`与`source_port`为指定查询源地址与端口，默认为查询设备IP地址和0  
`raise_on_no_answer`参数用于指定当查询无应答时是否出发异常，默认为True  


