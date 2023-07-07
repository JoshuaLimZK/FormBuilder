#!/bin/sh

export FLASK_APP=./server/server.py

flask --debug run -h 0.0.0.0 --port=6969
