##Install Kubernetes
https://www.kubeflow.org/docs/started/getting-started/#set-up-kubernetes

## Install Ksonnet
The ksonnet CLI ks, v0.9.2 or higher:
```
export KS_VER=0.11.0
export KS_BIN=ks_${KS_VER}_linux_amd64
wget -O /tmp/${KS_BIN}.tar.gz https://github.com/ksonnet/ksonnet/releases/download/v${KS_VER}/${KS_BIN}.tar.gz
mkdir -p ${HOME}/bin
tar -xvf /tmp/${KS_BIN}.tar.gz -C ${HOME}/bin
export PATH=${HOME}/bin/${KS_BIN}:$PATH

export KS_VER=0.13.1
export KS_BIN=ks_${KS_VER}_linux_amd64
wget -O /tmp/${KS_BIN}.tar.gz https://github.com/ksonnet/ksonnet/releases/download/v${KS_VER}/${KS_BIN}.tar.gz
mkdir -p ${HOME}/bin
tar -xvf /tmp/${KS_BIN}.tar.gz -C ${HOME}/bin
export PATH=${HOME}/bin/${KS_BIN}:$PATH
```

## Install Go
sudo snap install --classic go

## Setup Kubeflow
### Deploy Kubeflow
https://www.kubeflow.org/docs/started/getting-started/
```
KUBEFLOW_SRC=/home/constantine/space/src/hyperscaleai/3rdparty/kubeflow_src
mkdir ${KUBEFLOW_SRC}
cd ${KUBEFLOW_SRC}
export KUBEFLOW_TAG=v0.4.0-rc.2

curl https://raw.githubusercontent.com/kubeflow/kubeflow/${KUBEFLOW_TAG}/scripts/download.sh | bash
KFAPP=/home/constantine/space/src/hyperscaleai/3rdparty/kfapp
${KUBEFLOW_SRC}/scripts/kfctl.sh init ${KFAPP} --platform none
cd ${KFAPP}
${KUBEFLOW_SRC}/scripts/kfctl.sh generate k8s
${KUBEFLOW_SRC}/scripts/kfctl.sh apply k8s
```
ERROR: issues with kfctl =>
    RESOLVED: by upgrading ks version from 0.11 to 0.13


## Get sources
git clone https://github.com/kubeflow/examples /home/constantine/space/src/hyperscaleai/3rdparty/kubeflow_examples

## Install Kubeflow with Seldon
cd kubeflow_examples/github_issue_summarization
ks init ksonnet-kubeflow
cd ksonnet-kubeflow
cp ../ks-kubeflow/components/kubeflow-core.jsonnet components
cp ../ks-kubeflow/components/params.libsonnet components
cp ../ks-kubeflow/components/seldon.jsonnet components
cp ../ks-kubeflow/components/tfjob-v1alpha2.* components
cp ../ks-kubeflow/components/ui.* components