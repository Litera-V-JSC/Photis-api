#!/bin/sh

VOLUME_NAME="receipt_scanner"
IMAGE_NAME="receipt_scanner"

# Generate random data and hash it with sha256
SECRET_KEY=$(openssl rand -hex 32 | sha256sum | awk '{print $1}')

# Write to .env file
echo "SECRET_KEY=$SECRET_KEY" > .env

echo "[+] .env file created with SECRET_KEY"


# Check if the volume already exists
if docker volume ls -q | grep -w "$VOLUME_NAME" > /dev/null; then
  echo "[!] Volume '$VOLUME_NAME' already exists."
else
  echo "[+] Creating volume '$VOLUME_NAME'..."
  docker volume create "$VOLUME_NAME"
fi

docker build . -t $IMAGE_NAME:latest
echo "[+] Container build finished."
