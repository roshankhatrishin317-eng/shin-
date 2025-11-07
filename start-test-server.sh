#!/bin/bash

# Script to start the test server on port 4000

echo "Starting test server on http://localhost:4000"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is required but not found. Please install Python 3."
    exit 1
fi

# Check if port 4000 is already in use
if ss -tuln | grep -q ":4000 "
then
    echo "Warning: Port 4000 appears to be in use."
    echo "Process information:"
    ss -tulnp | grep ":4000 "
    echo
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    fi
fi

echo "Starting test server..."
python3 test-server.py