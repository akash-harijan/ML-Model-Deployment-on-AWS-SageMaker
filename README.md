# ML-Model-Deployment-on-AWS-SageMaker

Due to the scarcity of online resources about deployment of already trained ML model on AWS SageMaker, 
this project  except deployment using ipython notebooks. Notebook method doesn't provide flexibility.

## Installations

#### Pre-requisites

Ensure that awscli is installed, if not then install it
`pip install awscli 
`
. Once it is installled configure it with your aws access key and secret key
`aws configure`

#### DL-Model

ML model used here is cataract-detection, trained in keras. But any other model can be used by updating the code in 
folder CataractDetection. Weights of used model can be found here, [link]([here][https://raw.githubusercontent.com/akash-harijan/cataract-detection/master/models/final-700imgs.h5]
). This model is encapusalted in the Flask api with required format to deploy a model in sagemaker.

#### Dockerizatoin

Now it is time to create Docker of the ML model. 
`sudo deploy.sh`
It will create docker according to the docker file Dockerfile present in the directory. This deploy.sh script can 
be used to deploy the docker image to ECR as well, just turn on the upload_docker flag in file.

Lets test the created docker on a local machine with gpu.

`docker run --gpus all -p 8080:8080 -v /opt/ml:/opt/ml cataract-detection:latest serve`

- -p is used to map the port of local machine and docker image, as api is listeing on port 8080
- -v is used to map the path of local machine and docker image, as trained weights are placed at the path /opt/ml/model.
- serve file is the starting file of api. Number of processes of api can be changed in this file.

to test the api, run the script api_test.py
`python api_test.py`. It will predict the output that whether it is a normal image or cataract one. Images used in this
script are in test_imgs folder.

#### AWS Uploading

- Weights Upload: To upload the weights create a tar file containing the weights of trained model and upload it to a 
s3 bucket in aws. `tar -czvf test.tar.gz weights_file`
  
- Docker upload: To upload the docker image to aws, create an ecr repository and push the tested docker image to aws ecr,
deploy.sh script can be used to push the docker image to aws ecr.
  
#### SageMaker

There are three steps for the deployment on Sagemaker.
 1. *Creation of Model in SageMaker*: Go to the SageMaker menu in AWS and create a model with uploaded s3 bucket link and 
uploaded docker ecr link.
2. *Creation of Endpoint Configuration*: Create an endpoint configuration using model created in step no 1, also change
the ec2 instance type accordingly. ml.g4dn.xlarge is recommended for gpu usage.
3. *Creation of SageMaker Endpoint*: Create a SageMaker Endpoint from configuration created in step no 2.

It is assumed here that SageMaker endpoint is created, normally it takes around 10-15 minutes to get ready, it will 
show running status. 

To invoke the sagemaker endpoint use the script sagemaker_testing.py. But to use this script first install boto3 library. 

`pip install boto3`

`python sagemaker_testing.py`

[https://raw.githubusercontent.com/akash-harijan/cataract-detection/master/models/final-700imgs.h5]: https://raw.githubusercontent.com/akash-harijan/cataract-detection/master/models/final-700imgs.h5