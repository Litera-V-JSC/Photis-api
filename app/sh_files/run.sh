#!/bin/sh

VOLUME_NAME="receipt_scanner"
IMAGE_NAME="receipt_scanner"

echo "[+] Running container ..."
cd ..
docker run -p 8000:8000 --mount type=volume,source=$VOLUME_NAME,destination=/app/storage $IMAGE_NAME:latest