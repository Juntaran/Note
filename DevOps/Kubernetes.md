# Kubernetes

*学习 Kubernetes 是源于与韩飞师兄吃饭时的闲谈*   
*人生郁郁不得志，工作苦无出路，师兄建议我去学 k8s 找找乐子*  
*唉*  

## 一、Kubernetes 集群部署

### 1. 配置 VMware Fusion 环境:  

``` bash
sudo vim /Library/Preferences/VMware\ Fusion/vmnet8/dhcpd.conf

# 修改为以下配置

allow unknown-clients;
default-lease-time 1800;                # default is 30 minutes
max-lease-time 7200;                    # default is 2 hours

subnet 172.16.174.0 netmask 255.255.255.0 {
	range 172.16.174.130 172.16.174.140;
	option broadcast-address 172.16.174.255;
	option domain-name-servers 172.16.174.2;
	option domain-name localdomain;
	default-lease-time 1800;                # default is 30 minutes
	max-lease-time 7200;                    # default is 2 hours
	option netbios-name-servers 172.16.174.2;
	option routers 172.16.174.2;
}
host vmnet8 {
	hardware ethernet 00:50:56:C0:00:08;
	fixed-address 172.16.174.1;
	option domain-name-servers 0.0.0.0;
	option domain-name "";
	option routers 0.0.0.0;
}

host k8s_master {
    hardware ethernet 00:0c:29:7b:18:db;
    fixed-address 172.16.174.131;
}
host k8s_node_1 {
    hardware ethernet 00:0c:29:6c:59:7f;
    fixed-address 172.16.174.132;
}
host k8s_node_2 {
    hardware ethernet 00:0c:29:3f:bf:65;
    fixed-address 172.16.174.133;
}
```


### 2: kubeadm 安装 Kubernetes 1.8.1 

经过了一周自虐，本节只作为参考，建议所有在大陆的中国人选择第二种方式  
十九大期间在中国上外网，我真是石乐志，最后感谢阿里的开发者平台让我安装成功  

#### 2.1 准备工作

三台主机:  

```
vim /etc/hosts

172.16.174.131 node1
172.16.174.132 node2
172.16.174.133 node3
```

``` bash
systemctl disable firewalld
systemctl stop firewalld

modprobe bridge
modprobe br_netfilter

swapoff -a
```

```
vim /etc/sysctl.d/k8s.conf

net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
vm.swappiness=0
```

``` bash
sysctl -p /etc/sysctl.d/k8s.conf
setenforce 0
vim /etc/selinux/config
SELINUX=enforcing 改为 SELINUX=disabled
source /etc/selinux/config
```

```
vim /etc/fstab

# 注释掉下面这一行
/dev/mapper/centos-swap swap                    swap    defaults        0 0
```

更新 yum 源:  

``` bash
# 添加 163 源
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
cd /etc/yum.repos.d
wget http://mirrors.163.com/.help/CentOS7-Base-163.repo
yum clean all
yum makecache

# 添加 docker 源
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

安装 docker :  

``` bash
# 查看当前的 Docker 版本
yum list docker-ce.x86_64  --showduplicates |sort -r
```

Kubernetes 1.8 已经针对 Docker 的 `1.11.2`, `1.12.6`, `1.13.1` 和 `17.03.2` 等版本做了验证，在各节点安装 docker 的 `17.03.2` 版本  

``` bash
yum install -y --setopt=obsoletes=0 docker-ce-17.03.2.ce-1.el7.centos docker-ce-selinux-17.03.2.ce-1.el7.centos

systemctl start docker
systemctl enable docker

# Docker 从 1.13 版本开始调整了默认的防火墙规则，禁用了iptables filter 表中 FOWARD 链，这样会引起 Kubernetes 集群中跨 Node 的 Pod 无法通信
iptables -P FORWARD ACCEPT
```

``` bash
vim /lib/systemd/system/docker.service
# 增加
ExecStartPost=/usr/sbin/iptables -P FORWARD ACCEPT
```

``` bash
systemctl daemon-reload
systemctl restart docker
```

#### 2.2 下载 Kubernetes 相关镜像

阿里云镜像仓库
> 注册阿里云 registry https://dev.aliyun.com/search.html    
> 可以参考 https://yq.aliyun.com/articles/70756    

注册完之后在服务器登陆  

``` bash
docker login registry.cn-hangzhou.aliyuncs.com
```

16 个需要下载的镜像  

``` bash
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kube-apiserver-amd64:v1.8.1
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kube-controller-manager-amd64:v1.8.1
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kube-scheduler-amd64:v1.8.1
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kube-proxy-amd64:v1.8.1
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-sidecar-amd64:1.14.5
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-kube-dns-amd64:1.14.5
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-dnsmasq-nanny-amd64:1.14.5
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/etcd-amd64:3.0.17
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/pause-amd64:3.0
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kubernetes-dashboard-amd64:1.7.1
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kubernetes-dashboard-amd64:v1.7.1
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/kubernetes-dashboard-init-amd64:v1.0.1
docker pull registry.cn-shenzhen.aliyuncs.com/rancher_cn/heapster-influxdb-amd64:v1.3.3
docker pull registry.cn-shenzhen.aliyuncs.com/rancher_cn/heapster-grafana-amd64:v4.4.3
docker pull registry.cn-hangzhou.aliyuncs.com/google-containers/heapster-amd64:v1.4.2
docker pull registry.cn-hangzhou.aliyuncs.com/k8s_container/flannel:v0.9.0-amd64
```

重命名镜像以供 kubeadm 使用  

``` bash
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kube-apiserver-amd64:v1.8.1 gcr.io/google-containers/kube-apiserver-amd64:v1.8.1
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kube-controller-manager-amd64:v1.8.1 gcr.io/google-containers/kube-controller-manager-amd64:v1.8.1
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kube-scheduler-amd64:v1.8.1 gcr.io/google-containers/kube-scheduler-amd64:v1.8.1
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kube-proxy-amd64:v1.8.1 gcr.io/google-containers/kube-proxy-amd64:v1.8.1
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-sidecar-amd64:1.14.5 gcr.io/google-containers/k8s-dns-sidecar-amd64:1.14.5
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-kube-dns-amd64:1.14.5 gcr.io/google-containers/k8s-dns-kube-dns-amd64:1.14.5
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/k8s-dns-dnsmasq-nanny-amd64:1.14.5 gcr.io/google-containers/k8s-dns-dnsmasq-nanny-amd64:1.14.5
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/etcd-amd64:3.0.17 gcr.io/google-containers/etcd-amd64:3.0.17
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/pause-amd64:3.0 gcr.io/google-containers/pause-amd64:3.0
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kubernetes-dashboard-amd64:1.7.1 gcr.io/google-containers/kubernetes-dashboard-amd64:1.7.1
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kubernetes-dashboard-amd64:v1.7.1 gcr.io/google-containers/kubernetes-dashboard-amd64:v1.7.1
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/kubernetes-dashboard-init-amd64:v1.0.1 gcr.io/google-containers/kubernetes-dashboard-init-amd64:v1.0.1
docker tag registry.cn-shenzhen.aliyuncs.com/rancher_cn/heapster-influxdb-amd64:v1.3.3 gcr.io/rancher_cn/heapster-influxdb-amd64:v1.3.3
docker tag registry.cn-shenzhen.aliyuncs.com/rancher_cn/heapster-grafana-amd64:v4.4.3 gcr.io/rancher_cn/heapster-grafana-amd64:v4.4.3
docker tag registry.cn-hangzhou.aliyuncs.com/google-containers/heapster-amd64:v1.4.2 gcr.io/google-containers/heapster-amd64:v1.4.2
docker tag registry.cn-hangzhou.aliyuncs.com/k8s_container/flannel:v0.9.0-amd64 quay.io/coreos/flannel:v0.9.0-amd64
```


#### 2.3 安装并运行呢 Kubernetes 相关服务

``` bash
yum makecache fast
yum install -y kubelet kubeadm kubectl
```

``` bash
docker info | grep Cgroup
# 显示 Cgroup Driver: systemd
```

根据 docker info 的结果修改 kubeadm 的参数  

``` bash
vim /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

Environment="KUBELET_CGROUP_ARGS=--cgroup-driver=systemd"

# 创建 /etc/docker/daemon.json
vim /etc/docker/daemon.json

{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
```

``` bash
systemctl restart docker
systemctl status docker
systemctl enable kubelet.service
```

#### 2.4 Master 节点初始化

选择 `flannel` 作为 `Pod` 网络插件  
令 `node1` 为 Master Node，在 `node1` 执行以下命令  

``` bash
kubeadm init \
  --kubernetes-version=v1.8.1 \
  --pod-network-cidr=10.244.0.0/16 \
  --apiserver-advertise-address=172.16.174.131
```

#### 2.5 结果输出

```
kubeadm init --kubernetes-version=v1.8.1 --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=172.16.174.131

[kubeadm] WARNING: kubeadm is in beta, please do not use it for production clusters.
[init] Using Kubernetes version: v1.8.1
[init] Using Authorization modes: [Node RBAC]
[preflight] Running pre-flight checks
[preflight] Starting the kubelet service
[kubeadm] WARNING: starting in 1.8, tokens expire after 24 hours by default (if you require a non-expiring token use --token-ttl 0)
[certificates] Generated ca certificate and key.
[certificates] Generated apiserver certificate and key.
[certificates] apiserver serving cert is signed for DNS names [node1 kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 172.16.174.131]
[certificates] Generated apiserver-kubelet-client certificate and key.
[certificates] Generated sa key and public key.
[certificates] Generated front-proxy-ca certificate and key.
[certificates] Generated front-proxy-client certificate and key.
[certificates] Valid certificates and keys now exist in "/etc/kubernetes/pki"
[kubeconfig] Wrote KubeConfig file to disk: "admin.conf"
[kubeconfig] Wrote KubeConfig file to disk: "kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "controller-manager.conf"
[kubeconfig] Wrote KubeConfig file to disk: "scheduler.conf"
[controlplane] Wrote Static Pod manifest for component kube-apiserver to "/etc/kubernetes/manifests/kube-apiserver.yaml"
[controlplane] Wrote Static Pod manifest for component kube-controller-manager to "/etc/kubernetes/manifests/kube-controller-manager.yaml"
[controlplane] Wrote Static Pod manifest for component kube-scheduler to "/etc/kubernetes/manifests/kube-scheduler.yaml"
[etcd] Wrote Static Pod manifest for a local etcd instance to "/etc/kubernetes/manifests/etcd.yaml"
[init] Waiting for the kubelet to boot up the control plane as Static Pods from directory "/etc/kubernetes/manifests"
[init] This often takes around a minute; or longer if the control plane images have to be pulled.
[apiclient] All control plane components are healthy after 41.504266 seconds
[uploadconfig] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[markmaster] Will mark node node1 as master by adding a label and a taint
[markmaster] Master node1 tainted and labelled with key/value: node-role.kubernetes.io/master=""
[bootstraptoken] Using token: 3d97ad.4d01f99d0b28d473
[bootstraptoken] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstraptoken] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstraptoken] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstraptoken] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: kube-dns
[addons] Applied essential addon: kube-proxy

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run (as a regular user):

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  http://kubernetes.io/docs/admin/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join --token 3d97ad.4d01f99d0b28d473 172.16.174.131:6443 --discovery-token-ca-cert-hash sha256:a7b4d9e13897161b0a1d17577a29912b33b6519434ab81aeed2a2cd4d30f0158
```

最后执行  

``` bash
mkdir -p $HOME/.kubesudo 
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# 将节点加入集群
kubeadm join --token 3d97ad.4d01f99d0b28d473 172.16.174.131:6443 --discovery-token-ca-cert-hash sha256:a7b4d9e13897161b0a1d17577a29912b33b6519434ab81aeed2a2cd4d30f0158
```

如果因为网络等问题安装失败  

``` bash
# 查看问题
journalctl -xeu kubelet 

# 清理环境
kubeadm reset           
ifconfig cni0 down
ip link delete cni0
ifconfig flannel.1 down
ip link delete flannel.1
rm -rf /var/lib/cni/
```

init 如果报错  

```
[preflight] Some fatal errors occurred:
	/proc/sys/net/bridge/bridge-nf-call-iptables contents are not set to 1
[preflight] If you know what you are doing, you can skip pre-flight checks with `--skip-preflight-checks
```

执行

``` bash
echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
echo 1 > /proc/sys/net/bridge/bridge-nf-call-ip6tables
```

#### 2.6 搭建 etcd 高可用集群

*在 Master 节点执行*  

安装 cfssl  

``` bash
yum install go -y
go get -u github.com/cloudflare/cfssl/cmd/...
```

创建 ca-config.json :  

``` json
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "frognew": {
        "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ],
        "expiry": "87600h"
      }
    }
  }
}
```

创建 CA 证书签名请求配置 ca-csr.json :  

``` json
{
  "CN": "frognew",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "BeiJing",
      "L": "BeiJing",
      "O": "frognew",
      "OU": "cloudnative"
    }
  ]
}
```

cfss 生成 CA 证书和私钥  

```
~/go/bin/cfssl gencert -initca ca-csr.json | ~/go/bin/cfssljson -bare ca
```

创建 etcd 证书签名请求配置 etcd-csr.json :  

``` json
{
    "CN": "frognew",
    "hosts": [
      "127.0.0.1",
      "172.16.174.131",
      "172.16.174.132",
      "172.16.174.133",
      "node1",
      "node2",
      "node3"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "BeiJing",
            "L": "BeiJing",
            "O": "frognew",
            "OU": "cloudnative"
        }
    ]
}
```

生成 etcd 的证书和私钥:  

```
~/go/bin/cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=frognew etcd-csr.json | ~/go/bin/cfssljson -bare etcd
```

*在所有节点执行以下命令*  

``` bash 
mkdir -p /etc/etcd/ssl
```

*在 master 节点执行以下命令*

``` bash
scp *.pem root@172.16.174.131:/etc/etcd/ssl/
scp *.pem root@172.16.174.132:/etc/etcd/ssl/
scp *.pem root@172.16.174.133:/etc/etcd/ssl/
```

*在所有节点执行以下命令*  

``` bash
wget https://github.com/coreos/etcd/releases/download/v3.1.6/etcd-v3.1.6-linux-amd64.tar.gz
tar -zxvf etcd-v3.1.6-linux-amd64.tar.gz
mkdir -p /var/lib/etcd
mv etcd-v3.1.6-linux-amd64/etcd /usr/bin/
mv etcd-v3.1.6-linux-amd64/etcdctl /usr/bin/
```

``` bash
# 注意替换 node1 node2 node3, 172.16.174.131 172.16.174.132 172.16.174.133
export ETCD_NAME=node1
export INTERNAL_IP=172.16.174.131
```

``` bash
vim /usr/lib/systemd/system/etcd.service

[Unit]
Description=etcd server
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
WorkingDirectory=/var/lib/etcd/
EnvironmentFile=-/etc/etcd/etcd.conf
ExecStart=/usr/bin/etcd \
  --name ${ETCD_NAME} \
  --cert-file=/etc/etcd/ssl/etcd.pem \
  --key-file=/etc/etcd/ssl/etcd-key.pem \
  --peer-cert-file=/etc/etcd/ssl/etcd.pem \
  --peer-key-file=/etc/etcd/ssl/etcd-key.pem \
  --trusted-ca-file=/etc/etcd/ssl/ca.pem \
  --peer-trusted-ca-file=/etc/etcd/ssl/ca.pem \
  --initial-advertise-peer-urls https://${INTERNAL_IP}:2380 \
  --listen-peer-urls https://${INTERNAL_IP}:2380 \
  --listen-client-urls https://${INTERNAL_IP}:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://${INTERNAL_IP}:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster node1=https://172.16.174.131:2380,node2=https://172.16.174.132:2380,node3=https://172.16.174.133:2380 \
  --initial-cluster-state new \
  --data-dir=/var/lib/etcd
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

启动 etcd 

``` bash
systemctl daemon-reload
systemctl enable etcd
systemctl start etcd
systemctl status etcd
```


### 3. yum 安装 kubernetes 1.7

#### 3.1 一些准备工作

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

#### 3.2 163 替换自带 yum 源:  

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

#### 3.3 添加 virt7-container-common 源:  

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

#### 3.4 配置 etcd 与 docker

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

#### 3.5 配置 master

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

#### 3.6 配置 node

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

#### 3.7 校验

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

#### 3.8 安装 Flannel

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

#### 3.9 安装 heapster

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



#### 3.10 安装 dashboard

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