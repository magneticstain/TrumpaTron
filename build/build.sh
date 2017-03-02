#!/bin/bash

#
# TrumpaTron Build Script
#   - express build TrumpaTron for a given server
#

APP_DIR="/opt/trumpatron/"

# create directories
echo "Creating application directory..."
mkdir $APP_DIR > /dev/null 2>&1

# run any tests

# application runs
./trumpatron.py -t

echo "Build complete!"

exit 0