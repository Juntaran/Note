---
title: Go的并发机制.md
tags: Go,并发,Go并发编程实战
grammar_cjkRuby: true
---

**不要用共享内存的方式来通信，要以通信作为手段来共享内存**  
推荐使用通道(channel)在多个goroutine之间传递数据，并且还能够保证整个过程的并发安全


# goroutine

## go语句与goroutine

一条go语句意味着一个函数或方法的`并发`执行

如果要向go语句中传值，应该为go函数添加一个参数声明

    names := []string{"A", "B", "C"}
    for _, name := range names {
        go func(who string) {
        	fmt.Printf("%s\n", who)
        } (name)
    }
   
不加参数是不正确的

    names := []string{"A", "B", "C"}
    for _, name := range names {
        go func() {
        	fmt.Printf("%s\n", who)
        } ()
    }
    
go语句是在for循环执行完毕之后才执行的


# channel

channel提供了一种机制，  
既可以同步两个并发执行的函数，也可以让这两个函数通过相互传递特定类型的值来通信  

## channel的基本概念

channel既指`通道类型`，也指可以传递某种类型的值的`通道`  

### 类型表示法

与切片类型和字典类型相同，通道类型也属于引用类型

    chan T

`chan`代表了通道类型的关键字，`T`代表了通道类型的元素类型

    type IntChan chan int

别名类型`IntChan`代表了元素类型为`int`的`通道类型`

    var intChan chan int

初始化后，`intChan变量`可以用来传递`int`类型的元素值了  

上面这种声明方式意味着该通道类型是`双向`的，  
既可以向这个通道发送元素值，也可以从它接收元素值  

`单向通道`需要`接收操作符<-`  

    chan<- T

这是`只能用于发送值`的通道类型的泛化表示，`<-`表示元素值的流向  

    <-chan T

这是`只能用于接收值`的通道类型


### 值表示法

一个通道类型的变量在被初始化之前，其值一定是`nil`

### 操作特性

在同一时刻，仅有一个goroutine能向一个通道发送一个元素值，  
同时也仅有一个goroutine能从它那里接收值  
通道相当于一个`FIFO`的消息队列  
每个元素值都是严格按照发送到此的先后顺序排列的  
通道中的元素值具有`原子性`，不可分割，每一个元素值只能被某一个goroutine接收，  
已接收的元素值会立刻从通道中删除  

### 初始化通道

引用类型的值都需要使用内建函数`make`来初始化  

    make(chan int, 10)
    
这是一个最大缓冲为10的、传递元素类型为int的双向通道  
同样，也可以设置无缓冲通道，那么发送给它的元素值应该被立即取走，  
否则发送方的goroutine会阻塞，直到有接收方来接收



### 接收元素值

接收操作符<-不但可以作为通道类型声明的一部分，也可以用于通道操作

    strChan := make(chan string, 3)

此时，strChan是一个双向传递string类型的通道，容量为3  

    elem := <-strChan

把strChan的一个元素赋给变量elem

    elem, ok := <-strChan

这种也可以，ok为布尔类型，判断接收操作是否因通道关闭而失败  

**试图从一个未初始化的通道接收元素，会造成当前goroutine永久阻塞**


### 缓冲通道的规则

* 如果通道缓冲已满，发送goroutine会阻塞
* 如果通道缓冲为空，接收goroutine会阻塞
* 对于同一个元素值来说，把它发送给某个通道的操作，一定会在从该通道接收它的操作完成之前完成

### 发送元素值

    strChan <- "a"



