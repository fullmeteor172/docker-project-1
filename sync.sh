#!/usr/bin/env bash

REMOTE_USER="dhruv"
REMOTE_HOST="49.13.203.98"
REMOTE_DIR="/home/dhruv/projects/docker-project-1"

rsync -avz --delete \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='.venv' \
    ./ $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR