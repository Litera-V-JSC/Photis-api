#!/bin/bash

volume="receipt_scanner"
container="receipt_scanner:latest"

docker container run --rm -v "$volume:/source" -v "$(pwd):/backup" -w /source $container tar czf /backup/$volume.tar.gz .