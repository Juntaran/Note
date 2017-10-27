# Kubernetes

*学习 Kubernetes 是源于与韩飞师兄吃饭时的闲谈*   
*人生郁郁不得志，工作苦无出路，师兄建议我去学 k8s 找找乐子*  
*唉*  

## 一、Kubernetes 集群部署

### 1: 自残式安装 kubeadm 和相关工具 (经过了3天自虐，本节只作为参考，建议中国人选择第二种方式 19 大期间在中国上外网，我真是石乐志)

#### 1.1. 准备工作

```
systemctl disable firewalld
systemctl stop firewalld
setenforce 0

vim /etc/selinux/config
SELINUX=enforcing 改为 SELINUX=disabled
source /etc/selinux/config
```



``` bash
cd /etc/yum.repos.d
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
wget http://mirrors.163.com/.help/CentOS7-Base-163.repo
```

k8s.repo
```
[k8s]
name=Kubernetes Repository
baseurl=https://packages.cloud.googlecom/yum/repos/kubernetes-el7-x86_64
enabled=0
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
```

kubernetes.repo
```
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=0
```

mritd.repo
```
[mritd]
name=Mritd Repository
baseurl=https://yumrepo.b0.upaiyun.com/centos/7/x86_64
enabled=1
gpgcheck=1
gpgkey=https://mritd.b0.upaiyun.com/keys/rpm.public.key
```

``` sh
yum clean all
yum makecache
yum install -y docker kubelet kubeadm kubectl kubernetes-cni
systemctl enable docker && systemctl start docker
systemctl enable kubelet && systemctl start kubelet
```

`记住 kubelet 的版本，本文为 1.7.5`  

修改 docker 配置加速
```
vim /etc/sysconfig/docker
```

```
# /etc/sysconfig/docker

# Modify these options if you want to change the way the docker daemon runs
OPTIONS='--selinux-enabled --log-driver=journald --signature-verification=false --registry-mirror=http://68e02ab9.m.daocloud.io'
if [ -z "${DOCKER_CERT_PATH}" ]; then
    DOCKER_CERT_PATH=/etc/docker
fi

# Do not add registries in this file anymore. Use /etc/containers/registries.conf
# from the atomic-registries package.
#

# docker-latest daemon can be used by starting the docker-latest unitfile.
# To use docker-latest client, uncomment below lines
#DOCKERBINARY=/usr/bin/docker-latest
#DOCKERDBINARY=/usr/bin/dockerd-latest
#DOCKER_CONTAINERD_BINARY=/usr/bin/docker-containerd-latest
#DOCKER_CONTAINERD_SHIM_BINARY=/usr/bin/docker-containerd-shim-latest
```

重启 docker 服务

``` bash
service docker restart
```

#### 1.2. 下载 Kubernetes 相关镜像

阿里云镜像仓库
> 注册阿里云 registry https://dev.aliyun.com/search.html    
> 可以参考 https://yq.aliyun.com/articles/70756    

注册完之后在服务器登陆  

```
docker login registry.cn-hangzhou.aliyuncs.com
```

12 个需要下载的镜像  

```
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/pause-amd64:3.0
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/etcd-amd64:3.0.17
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kube-apiserver-amd64:v1.7.5
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kube-scheduler-amd64:v1.7.5
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kube-controller-manager-amd64:v1.7.5
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kube-proxy-amd64:v1.7.5
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/dnsmasq-metrics-amd64:1.0
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-kube-dns-amd64:1.14.5
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-dnsmasq-nanny-amd64:1.14.5
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-sidecar-amd64:1.14.5
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kube-discovery-amd64:1.0
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/exechealthz-amd64:1.2
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kubernetes-dashboard-amd64:v1.7.1
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kubedns-amd64:1.6
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/dnsmasq-metrics-amd64:1.0
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kube-dnsmasq-amd64:1.4
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/defaultbackend:1.0
```

重命名镜像以供 kubeadm 使用  

```
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/pause-amd64:3.0 gcr.io/google-containers/pause-amd64:3.0
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/etcd-amd64:3.0.17 gcr.io/google-containers/etcd-amd64:3.0.17
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kube-apiserver-amd64:v1.7.5 gcr.io/google-containers/kube-apiserver-amd64:v1.7.5
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kube-scheduler-amd64:v1.7.5 gcr.io/google-containers/kube-scheduler-amd64:v1.7.5
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kube-controller-manager-amd64:v1.7.5 gcr.io/google-containers/kube-controller-manager-amd64:v1.7.5
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kube-proxy-amd64:v1.7.5 gcr.io/google-containers/kube-proxy-amd64:v1.7.5
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/dnsmasq-metrics-amd64:1.0 gcr.io/google-containers/dnsmasq-metrics-amd64:1.0
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-kube-dns-amd64:1.14.5 gcr.io/google-containers/k8s-dns-kube-dns-amd64:1.14.5
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-dnsmasq-nanny-amd64:1.14.5 gcr.io/google-containers/k8s-dns-dnsmasq-nanny-amd64:1.14.5
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-sidecar-amd64:1.14.5 gcr.io/google-containers/k8s-dns-sidecar-amd64:1.14.5
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kube-discovery-amd64:1.0 gcr.io/google-containers/kube-discovery-amd64:1.0
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/exechealthz-amd64:1.2 gcr.io/google-containers/exechealthz-amd64:1.2
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kubernetes-dashboard-amd64:v1.7.1 gcr.io/google-containers/kubernetes-dashboard-amd64:v1.7.1
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kubedns-amd64:1.6 gcr.io/google-containers/kubedns-amd64:1.6
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/dnsmasq-metrics-amd64:1.0 gcr.io/google-containers/dnsmasq-metrics-amd64:1.0
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kube-dnsmasq-amd64:1.4 gcr.io/google-containers/kube-dnsmasq-amd64:1.4
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/defaultbackend:1.0 gcr.io/google-containers/defaultbackend:1.0
```

删除镜像

```
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/pause-amd64:3.0
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/etcd-amd64:3.0.17
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/kube-apiserver-amd64:v1.7.5
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/kube-scheduler-amd64:v1.7.5
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/kube-controller-manager-amd64:v1.7.5
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/kube-proxy-amd64:v1.7.5
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/dnsmasq-metrics-amd64:1.0
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-kube-dns-amd64:1.14.5
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-dnsmasq-nanny-amd64:1.14.5
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-sidecar-amd64:1.14.5
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/kube-discovery-amd64:1.0
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/exechealthz-amd64:1.2
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/kubernetes-dashboard-amd64:v1.7.1
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/kubedns-amd64:1.6
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/dnsmasq-metrics-amd64:1.0
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/kube-dnsmasq-amd64:1.4
docker rmi registry.cn-hangzhou.aliyuncs.com/google-containers/defaultbackend:1.0
```


#### 1.3. 运行 kubeadm init 安装 Master

``` bash
kubeadm init --kubernetes-version=v1.7.5
```

如果因为网络等问题安装失败  

``` bash
journalctl -xeu kubelet # 查看问题
kubeadm reset           # 清理环境
```

init 如果报错
```
[preflight] Some fatal errors occurred:
	/proc/sys/net/bridge/bridge-nf-call-iptables contents are not set to 1
[preflight] If you know what you are doing, you can skip pre-flight checks with `--skip-preflight-checks
```

执行

```
echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
echo 1 > /proc/sys/net/bridge/bridge-nf-call-ip6tables
```


### 2. 神 TM 安装 kubernetes  

#### 2.1 一些准备工作

```
systemctl disable firewalld
systemctl stop firewalld
setenforce 0

vim /etc/selinux/config
SELINUX=enforcing 改为 SELINUX=disabled
source /etc/selinux/config

hostnamectl --static set-hostname  kubernetes-master
hostnamectl --static set-hostname  kubernetes-node1
hostnamectl --static set-hostname  kubernetes-node2
```

修改 hosts 文件  

```
172.16.174.143 kubernetes-master
172.16.174.145 kubernetes-node1
172.16.174.142 kubernetes-node2
172.16.174.143 etcd
172.16.174.143 registry
```

#### 2.2 163 替换自带 yum 源:  

master 和 node 机器都要替换  

``` bash
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
cd /etc/yum.repos.d
wget http://mirrors.163.com/.help/CentOS7-Base-163.repo
yum clean all
yum makecache
```

找一个靠谱的源站： http://cbs.centos.org/  
搜索相应的包，本文直接搜索 `kubernetes` 即可，可以看到 1.7.6 版本的 kubernetes 对应的 tags `
virt7-container-common-candidate`  
在 http://cbs.centos.org/repos/ 找到即可，本文 yum 源 IP 为 http://cbs.centos.org/repos/virt7-container-common-candidate/x86_64/os/  

#### 2.3 添加 virt7-container-common 源:  

master 和 node 机器都要添加  

``` bash
vim /etc/yum.repos.d/k8s.repo
```

``` bash
[k8s]
name=virt7-testing
baseurl=http://cbs.centos.org/repos/virt7-container-common-candidate/x86_64/os/
gpgcheck=0
```

#### 2.4 配置 etcd 与 docker

`配置 docker`   
```
vim /etc/sysconfig/docker
```

```
OPTIONS='--selinux-enabled --log-driver=journald'
if [ -z "${DOCKER_CERT_PATH}" ]; then
    DOCKER_CERT_PATH=/etc/docker
fi
OPTIONS='--insecure-registry registry:5000'
```

```
systemctl enable docker
systemctl restart docker
```

`配置 etcd`  

``` bash
yum install etcd -y
```

etcd 在 `master` 上的配置  

``` bash
vim /etc/etcd/etcd.conf
```

```
ETCD_NAME=master
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379,http://0.0.0.0:4001"
ETCD_ADVERTISE_CLIENT_URLS="http://etcd:2379,http://etcd:4001"
```
验证 etcd  

```
systemctl start etcd
etcdctl set testdir/testkey0 0
etcdctl get testdir/testkey0
etcdctl -C http://etcd:4001 cluster-health
etcdctl -C http://etcd:2379 cluster-health
```

`安装 kubernetes`  

``` bash
yum -y install --enablerepo=k8s kubernetes
```

#### 2.5 配置 master

``` bash
vim /etc/kubernetes/apiserver
```

```
###
# kubernetes system config
#
# The following values are used to configure the kube-apiserver
#

# The address on the local server to listen to.
KUBE_API_ADDRESS="--insecure-bind-address=0.0.0.0"

# The port on the local server to listen on.
KUBE_API_PORT="--port=8080"

# Port minions listen on
# KUBELET_PORT="--kubelet-port=10250"

# Comma separated list of nodes in the etcd cluster
KUBE_ETCD_SERVERS="--etcd-servers=http://etcd:2379"

# Address range to use for services
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"

# default admission control policies
KUBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,LimitRanger,SecurityContextDeny,ResourceQuota,NamespaceExists"

# Add your own!
KUBE_API_ARGS=""
```


``` bash
vim /etc/kubernetes/config
```

```
###
# kubernetes system config
#
# The following values are used to configure various aspects of all
# kubernetes services, including
#
#   kube-apiserver.service
#   kube-controller-manager.service
#   kube-scheduler.service
#   kubelet.service
#   kube-proxy.service
# logging to stderr means we get it in the systemd journal
KUBE_LOGTOSTDERR="--logtostderr=true"

# journal message level, 0 is debug
KUBE_LOG_LEVEL="--v=0"

# Should this cluster be allowed to run privileged docker containers
KUBE_ALLOW_PRIV="--allow-privileged=false"

# How the controller-manager, scheduler, and proxy find the apiserver
KUBE_MASTER="--master=http://kubernetes-master:8080"
```

启动 kubernetes  

``` bash
systemctl enable kube-apiserver.service
systemctl start kube-apiserver.service
systemctl enable kube-controller-manager.service
systemctl start kube-controller-manager.service
systemctl enable kube-scheduler.service
systemctl start kube-scheduler.service
```

#### 2.6 配置 node

```
vim /etc/kubernetes/config
```

```
###
# kubernetes system config
#
# The following values are used to configure various aspects of all
# kubernetes services, including
#
#   kube-apiserver.service
#   kube-controller-manager.service
#   kube-scheduler.service
#   kubelet.service
#   kube-proxy.service
# logging to stderr means we get it in the systemd journal
KUBE_LOGTOSTDERR="--logtostderr=true"

# journal message level, 0 is debug
KUBE_LOG_LEVEL="--v=0"

# Should this cluster be allowed to run privileged docker containers
KUBE_ALLOW_PRIV="--allow-privileged=false"

# How the controller-manager, scheduler, and proxy find the apiserver
KUBE_MASTER="--master=http://kubernetes-master:8080"
```

``` bash
vim /etc/kubernetes/kubelet
```

```
###
# kubernetes kubelet (minion) config

# The address for the info server to serve on (set to 0.0.0.0 or "" for all interfaces)
KUBELET_ADDRESS="--address=0.0.0.0"

# The port for the info server to serve on
# KUBELET_PORT="--port=10250"

# You may leave this blank to use the actual hostname
KUBELET_HOSTNAME="--hostname-override=kubernetes-node1"

# location of the api-server
KUBELET_API_SERVER="--api-servers=http://kubernetes-master:8080"

# Add your own!
KUBELET_ARGS="--cgroup-driver=systemd"
```

启动 kubernetes  

``` bash
systemctl enable kubelet.service
systemctl start kubelet.service
systemctl enable kube-proxy.service
systemctl start kube-proxy.service
```

#### 2.7 校验

master 执行  
```
kubectl version
kubectl get nodes
kubectl -s http://kubernetes-master:8080 get node
```

你会发现一个讨厌的东西  

```
2017-10-26 20:32:21.787720 I | proto: duplicate proto type registered: google.protobuf.Any
2017-10-26 20:32:21.787779 I | proto: duplicate proto type registered: google.protobuf.Duration
2017-10-26 20:32:21.787792 I | proto: duplicate proto type registered: google.protobuf.Timestamp
```

这 TM 真的是 kubernetes 1.7 的 bug ！  

https://github.com/kubernetes/kubectl/issues/30
https://github.com/kubernetes/kubernetes/pull/52132
https://github.com/kubernetes/kubernetes/issues/48924

第三个 issus 下有人回复说升级 k8s 到 1.8.1 就好了  
算了。。不折腾了。。。心累  

#### 2.8 安装 Flannel

在 master 和 node 均需安装，配置相同  

``` bash
yum install flannel -y
```

```
vim /etc/sysconfig/flanneld
```

```
# Flanneld configuration options

# etcd url location.  Point this to the server where etcd runs
FLANNEL_ETCD_ENDPOINTS="http://etcd:2379"

# etcd config key.  This is the configuration key that flannel queries
# For address range assignment
FLANNEL_ETCD_PREFIX="/atomic.io/network"

# Any additional options that you want to pass
#FLANNEL_OPTIONS=""
```

在 master 上执行，注意网段  

``` bash
etcdctl mk /atomic.io/network/config '{ "Network": "172.16.174.0/8" }' { "Network": "172.16.174.0/8" }
```

重启服务  

master:  

``` bash
systemctl enable flanneld.service 
systemctl start flanneld.service 
service docker restart
systemctl restart kube-apiserver.service
systemctl restart kube-controller-manager.service
systemctl restart kube-scheduler.service
```

node:  

``` bash
systemctl enable flanneld.service 
systemctl start flanneld.service 
service docker restart
systemctl restart kubelet.service
systemctl restart kube-proxy.service
```

#### 2.9 安装 heapster

`部署 influxdb`:  

``` bash
cd /root/
git clone https://github.com/kubernetes/heapster.git
```
修改 `/root/heapster/deply/kube-config/influxdb/` 内所有的 `gcr.io` -> `registry.cn-hangzhou.aliyuncs.com`  

```
cd heapster/
kubectl create -f deploy/kube-config/influxdb/
kubectl create -f deploy/kube-config/rbac/heapster-rbac.yaml

kubectl get pods --namespace=kube-system
kubectl get services --namespace=kube-system monitoring-grafana monitoring-influxdb
```



#### 2.10 安装 dashboard

https://github.com/kubernetes/dashboard#kubernetes-dashboard  

``` bash 
wget https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
```

把这个 yaml 文件里所有的 `gcr.io` 都修改为 `registry.cn-hangzhou.aliyuncs.com`  

```
kubectl create -f kubernetes-dashboard.yaml
kubectl proxy
```
访问 http://127.0.0.1:8001/  

## 二. 问题记录：  

1. 别忘了 --namespace  

2. pods 无法删除时  

```
kubectl delete pods <unknown pods name> --grace-period=0 --force
```









___

## 附注:

手动安装 influxdb:  

新建 yum 源:  

``` bash
[influxdb]
name = InfluxDB Repository - RHEL \$releasever
baseurl = https://repos.influxdata.com/rhel/\$releasever/\$basearch/stable
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
```

```
yum install influxdb -y
systemctl enable influxdb
systemctl start influxdb
systemctl status influxdb
rpm -qc influxdb
```

一些简单测试:  

```
[root@localhost yum.repos.d]# influx
Connected to http://localhost:8086 version 1.3.5
InfluxDB shell version: 1.3.5
> SHOW DATABASES
name: databases
name
----
_internal
> CREATE DATABASE testdb
> SHOW DATABASES
name: databases
name
----
_internal
testdb
> use testdb
Using database testdb
> CREATE USER "root" WITH PASSWORD 'root' WITH ALL PRIVILEGES
> show users
user admin
---- -----
root true
> INSERT cpu,host=test,region=us_west value=0.64
> SELECT * FROM /.*/ LIMIT 1
name: cpu
time                host region  value
----                ---- ------  -----
1509025298119019129 test us_west 0.64
> quit()
```

___

## Refernece:  

* [yum 安装 Kubernetes 1.5](http://www.cnblogs.com/zhenyuyaodidiao/p/6500830.html)
* [CentOS 部署 Kubernetes 集群](https://www.kubernetes.org.cn/doc-16)
* [Flannel 解析](http://dockone.io/article/618)
* [kubespray 安装 Kubernetes](http://www.wisely.top/category/cloud-computing/kubernetes/)
* [Kubernetes 中文文档](http://hardocs.com/d/kubernetes/)
* [Kubernetes 中文文档_写的一般](https://www.kubernetes.org.cn/doc)