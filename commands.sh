#!/bin/bash

docker build --tag python-subtitle-generator . --build-arg var_name=Production
docker run --name python-subtitle-generator  -e "PORT=8000" -p 8007:8000 python-subtitle-generator