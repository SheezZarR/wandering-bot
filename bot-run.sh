#!/bin/sh

echo "Forwarding localhost to mongo"
socat TCP-LISTEN:27017,fork TCP:mongo:27017 &

echo "Starting python service..."
python src/main.py 


