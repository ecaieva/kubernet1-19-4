cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF


yum -y install kubeadm kubectl kubelet

systemctl enable kubelet.service

apt-cache madison kubeadm |grep 1.19

sudo apt install -y kubeadm=1.19.4-00 kubelet=1.19.4-00 kubectl=1.19.4-00

# cat pull-images.sh 
#!/bin/bash
images=(
	kube-apiserver:v1.19.4
	kube-controller-manager:v1.19.4
	kube-scheduler:v1.19.4
	kube-proxy:v1.19.4
	pause:3.2
	etcd:3.4.13-0
	coredns:1.7.0

)
for imageName in ${images[@]};
do
    docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/${imageName}
    docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/${imageName} k8s.gcr.io/${imageName}
    docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/${imageName}
done



# cat save-images.sh 
#!/bin/bash
images=(
    kube-apiserver:v1.19.4
	kube-controller-manager:v1.19.4
	kube-scheduler:v1.19.4
	kube-proxy:v1.19.4
	pause:3.2
	etcd:3.4.13-0
	coredns:1.7.0
)
for imageName in ${images[@]};
do
    docker save -o `echo ${imageName}|awk -F ':' '{print $1}'`.tar k8s.gcr.io/${imageName}
done



# cat load-image.sh 
#!/bin/bash
ls /root/kubeadm-images-1.19.4 > /root/images-list.txt
cd /root/kubeadm-images-1.19.4
for i in $(cat /root/images-list.txt)
do
     docker load -i $i
done


tar czvf kubeadm-images-1.19.4.tar.gz *.tar
tar czvf kubeadm-opt-images.tar.gz *.sh

卸载干净kube*
sudo apt-get purge --auto-remove kubeadm

sudo apt-get purge --auto-remove kubectl

sudo apt-get purge --auto-remove kubelet



apt-get install -y kubelet=1.19.4-00 kubeadm=1.19.4-00 kubectl=1.19.4-00

kubeadm config images list --kubernetes-version=v1.19.4
8s.gcr.io/kube-apiserver:v1.19.4
k8s.gcr.io/kube-controller-manager:v1.19.4
k8s.gcr.io/kube-scheduler:v1.19.4
k8s.gcr.io/kube-proxy:v1.19.4
k8s.gcr.io/pause:3.2
k8s.gcr.io/etcd:3.4.13-0
k8s.gcr.io/coredns:1.7.0



tar czvf coredns.tar.gz coredns.tar
tar czvf etcd.tar.gz etcd.tar
tar czvf kube-apiserver.tar.gz kube-apiserver.tar
tar czvf kube-controller-manager.tar.gz kube-controller-manager.tar
tar czvf kube-proxy.tar.gz kube-proxy.tar
tar czvf kube-scheduler.tar.gz kube-scheduler.tar
tar czvf pause.tar.gz pause.tar