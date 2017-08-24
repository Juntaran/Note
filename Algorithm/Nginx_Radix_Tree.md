# Nginx_Radix_Tree

*2017.8.21*

______

## 基础概念

Radix Tree 是一种多叉搜索树，每个结点有固定的孩子数（叉数 为2^n），可以快速定位叶子结点  

Nginx_Radix_Tree 是一种二叉查找树，叉数为2，它要求存储的每个节点必须以32位整型作为任意两节点的唯一标识  

基数树无需考虑树是否平衡，因此插入节点、删除节点的速度比红黑树快得多  

基数树可以不管树平衡的原因在于：  

> 红黑树是通过不同节点key关键字的比较决定树的形态  
> 而基数树的每个节点的key关键字自身已经决定了其在树中的位置  
> 先将节点的key关键字转化为二进制，32位，从左至右开始，遇0入左子树，遇1入右子树  

IP 可以转化为32位的二进制，因此描述一个 IP ，只需要深度32即可  
引入掩码后，利用掩码的1的个数来表示树的高度，可以减少很多浪费  

如果一个节点为 0x20000000 ，转化为二进制为 00100000 00000000 00000000 00000000  
0向左，1向右，所以 root->left->left->right  



## 源码

[ngx_radix_tree.h](https://trac.nginx.org/nginx/browser/nginx/src/core/ngx_radix_tree.h)  
[ngx_radix_tree.c](https://trac.nginx.org/nginx/browser/nginx/src/core/ngx_radix_tree.c)  

``` c
struct ngx_radix_node_s {
    ngx_radix_node_t  *right;
    ngx_radix_node_t  *left;
    ngx_radix_node_t  *parent;
    uintptr_t          value;       // 存储指针的值，指向用户自定义的数据结构
};


typedef struct {
    ngx_radix_node_t  *root;
    ngx_pool_t        *pool;        // 内存池，给基数树的节点分配内存
    ngx_radix_node_t  *free;        // 管理已经分配但不在树中的节点，free 实际上是所有不在树中节点的单链表
    char              *start;       // 已分配内存中还未使用的内存首地址
    size_t             size;        // 已分配内存中还未使用的内存大小
} ngx_radix_tree_t;
```

