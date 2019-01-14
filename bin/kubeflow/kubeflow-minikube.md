# Deploy Kubeflow on Minikube

## Install minikube

Please see [How to Minikube](https://gist.github.com/John-Lin/1dc063b6743f311561f2fe587e035c33)

## Running a minikube with 4CPUs and 8GB memory

```shell
$ minikube start --cpus 4 --memory 8192
```

If you want to use the vm driver with `hyperkit`

```shell
$ minikube start --vm-driver=hyperkit --cpus 4 --memory 8192
```

## Deploy Kubeflow

```shell
$ git clone git@github.com:google/kubeflow.git
$ cd kubeflow
$ kubectl apply -f components/ -R
# Wait until all pod are getting running state. (6-7 mins)
```

Get the URL for the notebook.

```shell
$ minikube service tf-hub-lb --url
```

or access JupyterHub on [http://localhost:8000](http://localhost:8000/) by

```shell
$ kubectl port-forward tf-hub-0 8000:8000
```

## User Login

input any username and password will login

## Basic notebook with scipy in JupyterHub 

###  Spawner options

**Image** : jupyter/scipy-notebook (jupyterhub version MUST be at least 0.8.1)

**CPU**: 200m (could be more)

**Memory**: 256Mi (could be more)

**Extra Resource Limits**: (leave it empty)

than press the **Spawn** button

##Tensorflow wit notebook in JupyterHub

###  Spawner options

**Image** : gcr.io/kubeflow/tensorflow-notebook-cpu

**CPU**: 300m (almost run out of quota in 4 CPU minikube)

**Memory**: 1.5Gi (could be more)

**Extra Resource Limits**: (leave it empty)

than press the **Spawn** button

### Running a tensorflow example

[See Neural Network Example](https://github.com/aymericdamien/TensorFlow-Examples/blob/master/notebooks/3_NeuralNetworks/neural_network_raw.ipynb)

You may get this message, python3.5 still works. but we are in 3.6 wait until google fixed this issue. We could just ignore.

```shell
/home/raju/anaconda3/lib/python3.6/importlib/_bootstrap.py:219: RuntimeWarning: compiletime version 3.5 of module 'tensorflow.python.framework.fast_tensor_util' does not match runtime version 3.6
```

See  https://github.com/tensorflow/tensorflow/issues/14182

## CPU/Mem resource monitoring on K8S 

```shell
$ kubectl describe node 
```