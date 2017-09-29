# 文件dos格式转unix格式

*2017.9.6*

windows 的文件上传到 linux 服务器总会有一些神奇的问题  

![dos_unix](https://raw.githubusercontent.com/Juntaran/Note/master/pictures/dos_unix.jpg)

如上图，vim 提示 `[noeol][dos]`  
如果是脚本的话，在执行的时候会提示 `/bin/sh^M: bad interpreter: No such file or directory`  

这些都是 windows 和 linux 编码格式不同的锅  
___

## 在 windows 端解决方案：  

打开 Notepad++ 【编码】->【以 UTF-8 无 BOM 格式编码】  

## 在 linux 端解决方案：  

vim 打开文件  

```bash  
:set ff
# 或者是
:set fileformat
```

会显示  
```bash
# windows
fileformat=dos
# linux
fileformat=unix
```

强制转换为 unix 格式  
```bash
:set ff-unix
```

脚本：  
```bash
vi +':w ++ff=unix' +':q' test.txt

# ^M 为 Ctrl+V+M ，表示回车
sed 's/^M//' dos.txt > tmp_filename
```


___
## Reference:  

* [关于 DOS 文件转换成 UNIX 文件格式](http://ju.outofmemory.cn/entry/56461)
* [sh 脚本异常](http://www.cnblogs.com/pipelone/archive/2009/04/17/1437879.html)