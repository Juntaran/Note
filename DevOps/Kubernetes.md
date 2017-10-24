# Kubernetes

*学习 Kubernetes 是源于与韩飞师兄吃饭时的闲谈*   
*人生郁郁不得志，工作苦无出路，师兄建议我去学 k8s 找找乐子*  
*唉*  

## 一、Kubernetes 集群部署

### 1. 安装 kubeadm 和相关工具

``` bash
cd /etc/yum.repos.d
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

### 2. 下载 Kubernetes 相关镜像

阿里云镜像仓库
> 注册阿里云 registry https://dev.aliyun.com/search.html    
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
```

### 3. 运行 kubeadm init 安装 Master

``` bash
kubeadm init --kubernetes-version=v1.7.5
```
