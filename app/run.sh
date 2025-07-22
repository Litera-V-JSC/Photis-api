#!/bin/sh

VOLUME_NAME="receipt_scanner"
IMAGE_NAME="receipt_scanner"

# Check if the volume already exists
if docker volume ls -q | grep -w "$VOLUME_NAME" > /dev/null; then
  echo "[!] Volume '$VOLUME_NAME' already exists."
else
  echo "[+] Creating volume '$VOLUME_NAME'..."
  docker volume create "$VOLUME_NAME"
fi

echo "[+] Running container ..."
docker run -p 8000:8000 --mount type=volume,source=$VOLUME_NAME,destination=/app/storage $IMAGE_NAME:latest