export KS_VER=0.13.1
export KS_BIN=ks_${KS_VER}_linux_amd64
export PATH=${HOME}/bin/${KS_BIN}:$PATH

git clone https://github.com/katacoda/kubeflow-examples.git examples; cd examples/github_issue_summarization/ks-kubeflow

NAMESPACE=kubeflow
ks env add tfjob-run1 -n $NAMESPACE
ks env set tfjob-run1 -n $NAMESPACE
ks apply tfjob-run1 -c data-pvc -n $NAMESPACE
ks apply tfjob-run1 -c data-downloader -n $NAMESPACE
ks apply tfjob-run1 -c tfjob-pvc-v1alpha2 -n $NAMESPACE


kubectl get pods -l job-name -n $NAMESPACE

ks param set tfjob namespace default

ks param set tfjob namespace $NAMESPACE
ks param set tfjob image "gcr.io/agwl-kubeflow/tf-job-issue-summarization:latest"
ks param set tfjob sample_size 100000

# Serving Model
Once the trained model (_outputmodel.h5) is available, it needs to be packaged up as a Docker Image. As the serving will be done via Seldon Core, the command below would build the required Docker Image containing your trained model. This has been done for you and uploaded as gcr.io/kubeflow-images-public/issue-summarization:0.1.

The commands below represent what's required to build the image.
```
docker run -v $(pwd)/my_model/:/my_model seldonio/core-python-wrapper:0.7 \
 /my_model IssueSummarization 0.1 gcr.io --base-image=python:3.6 \
 --image-name=gcr-repository-name/issue-summarization

cd build
./build_image.sh
```
docker run -v $(pwd)/my_model/:/my_model seldonio/core-python-wrapper:0.7 /my_model IssueSummarization 0.1 gcr.io --base-image=python:3.6 --image-name=gcr-repository-name/issue-summarization

ks pkg install kubeflow/seldon