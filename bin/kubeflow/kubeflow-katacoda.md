# What is Kubeflow?
The Kubeflow project is dedicated to making Machine Learning easy to set up with Kubernetes, portable and scalable. The goal is not to recreate other services, but to provide a straightforward way for spinning up best of breed OSS solutions. Kubernetes is an open-source platform for automating deployment, scaling, and management of containerised applications.

Because Kubeflow relies on Kubernetes, it runs wherever Kubernetes runs such as bare-metal servers, or cloud providers such as Google. Details of the project can be found at https://github.com/kubeflow/kubeflow

## Kubeflow Components
Kubeflow has three core components.

### TF Job Operator and Controller: 
Extension to Kubernetes to simplify deployment of distributed TensorFlow workloads. By using an Operator, Kubeflow is capable of automatically configuring the master, worker and parameterized server configuration. Workloads can be deployed with a TFJob.

### TF Hub: 
Running instances of JupyterHub, enabling you to work with Jupyter Notebooks.

### Model Server: 
Deploying a trained TensorFlow models for clients to access and use for future predictions.

These three models will be used to deploy different workloads in the following steps.

# Deploy Kubeflow
```
export GITHUB_TOKEN=99510f2ccf40e496d1e97dbec9f31cb16770b884

export KUBEFLOW_VERSION=0.2.5
curl https://raw.githubusercontent.com/kubeflow/kubeflow/v${KUBEFLOW_VERSION}/scripts/deploy.sh | bash

kubectl get pods

kubectl apply -f ~/kubeflow/katacoda.yaml

```

# Deploy TensorFlow Job (TFJob)

TfJob provides a Kubeflow custom resource that makes it easy to run distributed or non-distributed TensorFlow jobs on Kubernetes. The TFJob controller takes a YAML specification for a master, parameter servers, and workers to help run distributed computation.

A Custom Resource Definition (CRD) provides the ability to create and manage TF Jobs in the same fashion as built-in Kubernetes resources. Once deployed, the CRD can configure the TensorFlow job, allowing users to focus on machine learning instead of infrastructure.

## Create TFJob Deployment Definition
To deploy the TensorFlow workload described in the previous step, Kubeflow needs a TFJob definition. In this scenario, you can view it by running 
```
cat example.yaml
```

The definition defines three components:

### Master: 
Each job must have one master. The master will coordinate training operations execution between workers.

### Worker: 
A job can have 0 to N workers. Each worker process runs the same model, providing parameters for processing to a Parameter Server.

### PS: 
A job can have 0 to N parameter servers. Parameter server enables you to scale your model across multiple machines.

More information can be found at https://www.tensorflow.org/deploy/distributed

## Deploying TFJob
The TFJob can be deployed by running 
```
kubectl apply -f example.yaml
```
By deploying the job, Kubernetes will schedule the workloads for execution across the available nodes. As part of the deployment, Kubeflow will configure TensorFlow with the required settings allowing the different components to communicate.

The next step will explain the Job and how to access the results.

# View Job Progress and Results
The status of TensorFlow jobs can be viewed via 
```kubectl get tfjob``` 
Once the TensorFlow job has been completed, the master is marked as successful. 
Keep running the job command to see when it finishes.

The master is responsible for coordinating the execution and aggregating the results. Under the covers, the completed workloads can be listed using 
```
kubectl get pods | grep Completed
```

In this example, the results are outputted to STDOUT, viewable using kubectl logs.

The command below will output the results:
```
kubectl logs $(kubectl get pods | grep Completed | tr -s ' ' | cut -d ' ' -f 1)
```
You will see the results from the execution of the workload on the master, worker and parameter servers.



# Deploy JupyterHub
The second key component of Kubeflow is the ability to run Jupyter Notebooks via JupyterHub. 
Jupyter Notebook is the classic data science tool to run inline scripts and code snippets 
while documenting the process in the browser.

With Kubeflow the JupyterHub is deployed onto the Kubernetes cluster. 
You can find there the Load Balancer IP address using kubectl get svc

Open Jupyter Hub
Via Katacoda, you can access the browser interface at the following link 
https://2886795269-80-frugo04.environments.katacoda.com or using the terminal Jupyterhub tab. 
To access the JupyterHub use the username admin and a blank password in the login form.

To deploy a notebook, a new server has to be started. 
Kubeflow is using internally the gcr.io/kubeflow-images-public/tensorflow-1.8.0-notebook-cpu:v0.2.1 
Docker Image as default. After accessing the JupyterHub, you can click Start My server button.

The server launcher allows you to configure additional options, such as resource requirements. In this case, accept the defaults and click Spawn to start the server. Now you can see the contents of the Docker image that you can navigate, extend and work with Jupyter Notebooks.

Under the covers, this will Spawn a new Kubernetes Pod called jupyter-admin for managing the server. View this using kubectl get pods jupyter-admin

Working with Jupyter Notebook
JupyterHub can now be accessed via the pod. You can now work with the environment seamlessly. For example to create a new notebook, select the New dropdown, and select the Python 3 kernel as shown below.

Create New Jupyter Notebook

It's now possible to create code snippets. To start working with TensorFlow, paste the code below to the first cell and run it.

Copy to Clipboardfrom __future__ import print_function

import tensorflow as tf

hello = tf.constant('Hello TensorFlow!')
s = tf.Session()
print(s.run(hello))

# Access Model Server
The final Component is the model server. Once trained, the model can be used to perform 
predictions for the new data when it's published. By using Kubeflow, it's possible 
to access the server by deploying jobs to the Kubernetes infrastructure.

## Deploy Trained Model Server
The Kubeflow tf-serving provides the template for serving a TensorFlow model. 
This can be customised and deployed by using Ksonnet and defining the parameters based on your model.

Using environment variables, we're defining the names and path of where our trained model is located.
```
MODEL_COMPONENT=model-server
MODEL_NAME=inception
MODEL_PATH=/serving/inception-export
```
Using Ksonnet, it's possible to extend the Kubeflow tf-serving component to match the requirements for the model.
```
cd ~/kubeflow_ks_app
ks generate tf-serving ${MODEL_COMPONENT} --name=${MODEL_NAME}
ks param set ${MODEL_COMPONENT} modelPath $MODEL_PATH

ks param set ${MODEL_COMPONENT} modelServerImage katacoda/tensorflow_serving
```
The parameters defined can be viewed via 
```
ks param list
```

This provides a script that can be deployed to the environment and make our model available to clients.

You can deploy the template to the defined Kubernetes cluster.
```
ks apply default -c ${MODEL_COMPONENT}
```
Clients will now be able to connect and access the trained data, see the pod running via kubectl get pods

## Image Classification
In this example, we use the pre-trained Inception V3 model. It's the architecture trained on ImageNet dataset. The ML task is image classification while the model server and its clients being handled by Kubernetes.

To use the published model, you need to set up the client. This can be achieved the same way as other jobs. The YAML file for deploying the client is cat ~/model-client-job.yaml. To deploy it use the following command:
```
kubectl apply -f ~/model-client-job.yaml
```
To see the status of the model-client-job run:
```
kubectl get pods
```
The command below will output the classification results for the Katacoda logo.
```
kubectl logs $(kubectl get pods | grep Completed | tail -n1 |  tr -s ' ' | cut -d ' ' -f 1)
```
More information on serving models via Kubernetes can be found at https://github.com/kubeflow/kubeflow/tree/master/components/k8s-model-server