#!/bin/sh

name="intactness-pipeline-container"

function _build {
    # current --platform is for M-series macbooks
    # Windows users use        --platform darwin/amd64
    # linux users use          --platform linux/amd64
    docker build -t "$name" ./ --platform linux/amd64
}

function _start {
    #port 8181
    docker run -dit -p 8181:8181 \
        --name "$name" \
        -v "$PWD":/app \
        "$name"
    docker ps
}

function _stop {
    docker stop "$name"
}

function _remove {
    _stop
    docker rm "$name"
}

if [ $1 = "build" ]; then
   _build
elif [ $1 = "start" ]; then
   _start
elif [ $1 = "rebuild" ]; then
    _remove
    _build
    _start
elif [ $1 = "stop" ]; then
    _stop
elif [ $1 = "remove" ]; then
    _remove
elif [ $1 = "bash" ]; then
    docker exec -it "$name" bash
fi