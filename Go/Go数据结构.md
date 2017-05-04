---
title: Go数据结构
tags: Go,数据结构
---


1. `数组`是`slice`和`map`的底层结构

2. `slice`是Go里面惯用的集合数据的方法，`map`则是用来存储键值对

3. 内建函数`make`用来创建`slice`和`map`，并且为它们指定长度和容量等等。`slice和`map`字面值也可以做同样的事

4. `slice`有`容量`的`约束`，不过可以通过内建函数`append`来增加元素

5. `map`没有`容量`一说，所以也没有任何增长限制

6. 内建函数`len`可以用来获得`slice`和`map`的长度

7. 内建函数`cap`只能作用在`slice`上

8. 可以通过组合方式来创建多维数组和`slice`。`map`的值可以是`slice`或者另一个`map`。`slice`不能作为`map`的键

9. 在函数之间传递`slice`和`map`是相当廉价的，因为他们不会传递底层数组的拷贝

___
Reference:
* [studyGolang.com](http://studygolang.com/articles/2335)
