#!/bin/bash


#Update the system packages
sudo apt update

#Install Docker
sudo apt install -y docker.io

#Start and enable the Docker service
sudo systemctl enable --now docker
sudo systemctl start docker

#Pull your monitor image (from ECR later — for now we'll use a placeholder)

#Run the container with port 8000 exposed and the DISCORD_WEBHOOK_URL env var passed in
sudo docker run -d \
    -p 8000:8000 \
    -e DISCORD_WEBHOOK_URL="${DISCORD_WEBHOOK_URL}" \
    ghcr.io/Mascotte33/system-monitor:latest






### TASK for someday, create a script that will check what linux you are on and act accordingly