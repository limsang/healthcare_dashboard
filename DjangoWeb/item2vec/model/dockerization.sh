#!/bin/bash


$(aws ecr get-login --region ap-northeast-2 --no-include-email)
docker build -f $PWD/no-cuda/dockerfile -t appipe-rnd-recsys-item2vec $PWD
docker tag appipe-rnd-recsys-item2vec:latest 148537736837.dkr.ecr.ap-northeast-2.amazonaws.com/appipe-rnd-recsys-item2vec:latest
docker push 148537736837.dkr.ecr.ap-northeast-2.amazonaws.com/appipe-rnd-recsys-item2vec:latest


#docker run ap-recsys-item2vec:latest
