#!/bin/bash


create_docker=1
upload_docker=0


echo Creating Docker ------------------------------------------------------------

if [[ $create_docker -eq 1 ]]
then
  TAG=latest
  SERVING_REPOSITORY=cataract-detection

  docker build --file Dockerfile --tag $SERVING_REPOSITORY:$TAG .
fi


if [[ $upload_docker -eq 1 ]]
then
  echo Pushing to AWS ------------------------------------------------------------
  ECR_REPO_NAME='311758178562.dkr.ecr.us-east-1.amazonaws.com/akash-testing'
  ECR_REPO_TAG='test'

  output=$(aws ecr get-login --no-include-email)
  $output
  docker_id=$(docker images | grep $SERVING_REPOSITORY |awk '{print $3}')
  docker tag $docker_id $ECR_REPO_NAME:$ECR_REPO_TAG
  docker push $ECR_REPO_NAME:$ECR_REPO_TAG
fi