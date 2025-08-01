#!/bin/bash

volume="photis"
container="photis:latest"

docker container run --rm -v "$volume:/source" -v "$(pwd):/backup" -w /source $container tar czf /backup/$volume.tar.gz .