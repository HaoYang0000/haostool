#!/usr/bin/env bash

ROOT=/Volumes/CODE/notifications

cd "${ROOT}"

docker-compose build
docker-compose up -d
