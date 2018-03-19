# Linux大文件生成

*2017.7.24*


首先问题来了，为什么要生成大文件呢  

生成大文件可以做一些测试，比如系统性能啦~  

好了，加入当前磁盘大小为 20G ，系统组要求磁盘利用率达到 30% ，已用 3G    
那么我们还需要生成 3G 的文件~  

``` bash
dd if=/dev/zero of=test bs=1M count=3000
```

系统组的同学可以用以下方法来检测到~

``` bash
find -type f -size +500M    # 查找大于500M的文件
```

这里文件大小的单位可以使用 `b`，`k`，`M`，`G`  

  
于是乎我们可以反其道而行之，生成 3000 个 1M 的文件~  

``` bash
seq 3000 | xargs -i dd if=/dev/zero of={}.dat bs=1024000 count=1
```

如果机智的话，其实他们还是可以发现的  

``` bash
du --max-depth=1 | sort -rn    # 按从大到小的顺序对目录进行排序
```

______

网上还有一个丧心病狂的命令  

``` bash
dd if=/dev/zero of=test bs=1M count=0 seek=100000
```

创建的文件在文件系统中的显示大小为 100000MB ，但是并不实际占用 block ，因此创建速度与内存速度相当，seek 的作用是跳过输出文件中指定大小的部分，这就达到了创建大文件，但是并不实际写入的目的。当然，因为不实际写入硬盘，所以你在容量只有 10G 的硬盘上创建 100G 的此类文件都是可以的


______

## dd 命令

|  参数  |  说明  |
|----|----|
| if=filename   | 输入文件名，缺省为标准输入  |
| of=filename   | 输出文件名，缺省为标准输出   |
| ibs=bytes   |  一次读入 bytes 个字节(即一个块大小为 bytes 个字节)  |
| obs=bytes   |  一次写 bytes 个字节(即一个块大小为 bytes 个字节)  |
| bs=bytes   |  同时设置读写块的大小为 bytes ，可代替 ibs 和 obs  |
| cbs=bytes   |  一次转换 bytes 个字节，即转换缓冲区大小  |
| skip=blocks   |  从输入文件开头跳过 blocks 个块后再开始复制  |
| seek=blocks   |  从输出文件开头跳过 blocks 个块后再开始复制(通常只有当输出文件是磁盘或磁带时才有效)  |
|  count=blocks  |  仅拷贝 blocks 个块，块大小等于 ibs 指定的字节数  |
|  conv=conversion  |  指定的参数转换文件  |

______

## Reference:
* [Cynric](http://blog.csdn.net/cywosp/article/details/9674757)
* [dd命令使用详解](http://www.cnblogs.com/qq78292959/archive/2012/02/23/2364760.html)