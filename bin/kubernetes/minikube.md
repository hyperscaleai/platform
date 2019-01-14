# Minikube

## Installation

```shell
$ curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.24.0/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```

## Quickstart

```shell
# macOS
$ minikube start --vm-driver=hyperkit
# or
$ minikube start --vm-driver=virtualbox

# Linux
$ minikube start --vm-driver=kvm2
# or
$ minikube start --vm-driver=virtualbox
# or 
$ minikube start --vm-driver=none
# runs the Kubernetes components on the host and not in a VM. Docker is required to use this driver but no hypervisor
```

## Services, Status & Showing IPs

```shell
$ minikube ip
192.168.64.5

$ minikube status
minikube: Running
cluster: Running
kubectl: Correctly Configured: pointing to minikube-vm at 192.168.64.5


minikube service list

# To access a service exposed via a node port
# Open a browser for cv-server service
$ minikube service cv-server

# To access the Kubernetes Dashboard
$ minikube dashboard
```

##  Kubectl context

```shell
$ kubectl config use-context minikube
# or 
$ kubectl get pods --context=minikube
```

## Logs & Monitoring
```
kubectl describe node 
kubectl logs <pod> 
```

## Stop, Destroy & Cleanup

```shell
$ minikube stop
$ minikube delete
$ rm -rf ~/.minikube
```