# Prerequisites
1. Minikube installed = via snap
2. Ksonnet installed 
= https://github.com/ksonnet/ksonnet/releases (download and copy to /usr/bin/ks)

## Install Ksonnet
The ksonnet CLI ks, v0.9.2 or higher:
```
export KS_VER=0.13.1
export KS_BIN=ks_${KS_VER}_linux_amd64
wget -O /tmp/${KS_BIN}.tar.gz https://github.com/ksonnet/ksonnet/releases/download/v${KS_VER}/${KS_BIN}.tar.gz
mkdir -p ${HOME}/bin
tar -xvf /tmp/${KS_BIN}.tar.gz -C ${HOME}/bin
export PATH=${HOME}/bin/${KS_BIN}:$PATH

export KS_VER=0.13.1
export KS_BIN=ks_${KS_VER}_linux_amd64
export PATH=${HOME}/bin/${KS_BIN}:$PATH

```

# Deploy Kubeflow

KF_ENV=cloud|nocloud
KF_ENV=nocloud
## Create namespace
NAMESPACE=kubeflow
kubectl create namespace ${NAMESPACE}

## initialize ksonnet app
APP_NAME=my-kubeflow
ks init ${APP_NAME}

ERROR:
```
panic: runtime error: invalid memory address or nil pointer dereference                                                                                                                                                                                                         
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x456452]                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                              
goroutine 1 [running]:

ref: https://github.com/ksonnet/ksonnet/issues/883
```
SOLUTION: >> update ksonnet to 13.+ and install go
VERIFICATION:
```
$ kubectl version
Client Version: version.Info{Major:"1", Minor:"12", GitVersion:"v1.12.4", GitCommit:"f49fa022dbe63faafd0da106ef7e05a29721d3f1", GitTreeState:"clean", BuildDate:"2018-12-14T07:10:00Z", GoVersion:"go1.10.4", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"12", GitVersion:"v1.12.4", GitCommit:"f49fa022dbe63faafd0da106ef7e05a29721d3f1", GitTreeState:"clean", BuildDate:"2018-12-14T06:59:37Z", GoVersion:"go1.10.4", Compiler:"gc", Platform:"linux/amd64"}

$ ks version

ksonnet version: 0.13.1
jsonnet version: v0.11.2
client-go version: kubernetes-1.10.4

```

cd ${APP_NAME}
ks env set default --namespace ${NAMESPACE}

##Install kubeflow components

export GITHUB_TOKEN=99510f2ccf40e496d1e97dbec9f31cb16770b884

ks registry add kubeflow github.com/katacoda/kubeflow-ksonnet/tree/master/kubeflow
ks pkg install kubeflow/argo
ks pkg install kubeflow/core
ks pkg install kubeflow/seldon
ks pkg install kubeflow/tf-serving

```
OR ALTERNATIVELY:
ks registry add kubeflow github.com/kubeflow/kubeflow/tree/${VERSION}/kubeflow

ks pkg install kubeflow/core@${VERSION}
ks pkg install kubeflow/tf-serving@${VERSION}
ks pkg install kubeflow/tf-job@${VERSION}

```

# Create templates for core components
ks generate kubeflow-core kubeflow-core --namespace=${NAMESPACE}
```
# If your cluster is running on Azure you will need to set the cloud parameter.
# If the cluster was created with AKS or ACS choose aks, it if was created
# with acs-engine, choose acsengine
# PLATFORM=<aks|acsengine>
# ks param set kubeflow-core cloud ${PLATFORM}

# Enable collection of anonymous usage metrics
# Skip this step if you don't want to enable collection.
```
ks param set kubeflow-core reportUsage false
kubectl delete -n ${NAMESPACE} deploy spartakus-volunteer

## Deploy Kubeflow
ks apply default -c kubeflow-core

## create persistance volume and services for katacoda (app???)

remove HOST_IP, HOST2_IP
modify katacoda.yaml - update data=>~/data
kubectl apply -f /home/constantine/space/src/hyperscaleai/3rdparty/katakoda/kubeflow-ksonnet/katacoda.yaml -n ${NAMESPACE}

## view status
kubectl get pods -n ${NAMESPACE}

# Create TFJob Deployment Definition
cat /home/constantine/space/src/hyperscaleai/3rdparty/katakoda/kubeflow-ksonnet/example-distributed-tfjob.yaml

## Start distributed TFJob
kubectl apply -f example-dsitributed-tfjob.yaml -n $NAMESPACE && kubectl get tfjob -n $NAMESPACE && kubectl get pods-n $NAMESPACE 

## View status progress
kubectl get tfjob && kubectl get pods

kubectl get pods -n $NAMESPACE --no-headers -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}' | grep master | xargs kubectl logs -f

(OPTIONAL)
kubectl delete -f example-dsitributed-tfjob.yaml -n $NAMESPACE


# JupyterHub
## init port forwarding
https://github.com/kubeflow/kubeflow/tree/master/components/jupyterhub

kubectl port-forward tf-hub-0 8000:8000 --namespace $NAMESPACE

ks param set kubeflow-core jupyterNotebookPVCMount /home/jovyan

ks prototype describe jupyterhub
kubectl get svc
kubectl get svc -n=${NAMESPACE}

access http://localhost (OR EXTERNAL IP):8000
admin/admin and spawn new jupyter notebook instance
wait until created
kubectl get pods


### NodePort (for non-cloud) by issuing

ks param set kubeflow-core jupyterHubServiceType NodePort
ks apply ${KF_ENV}
### LoadBalancer (for cloud) by issuing
ks param set kubeflow-core jupyterHubServiceType LoadBalancer
ks apply ${KF_ENV}

## Monitoring
https://github.com/kubeflow/examples/tree/master/mnist

# Serving with TF-Serving


## deploy 01
MODEL_COMPONENT=model-server
MODEL_NAME=inception
MODEL_PATH=/serving/inception-export

cd /home/constantine/space/src/hyperscaleai/3rdparty/katakoda/kubeflow-ksonnet/my-kubeflow
ks generate tf-serving ${MODEL_COMPONENT} --name=${MODEL_NAME}
ks param set ${MODEL_COMPONENT} modelPath $MODEL_PATH 
ks param set ${MODEL_COMPONENT} modelServerImage katacoda/tensorflow_serving

ks param list

### deploy model
ks apply default -c ${MODEL_COMPONENT}
kubectl get pods --namespace=${NAMESPACE}


## deploy InceptionV3
cat model-client-job.yaml

kubectl apply -n ${NAMESPACE} -f model-client-job.yaml

kubectl get pods -n ${NAMESPACE}

kubectl logs -n ${NAMESPACE} $(kubectl get pods -n ${NAMESPACE} | grep Completed | tail -n1 |  tr -s ' ' | cut -d ' ' -f 1)

