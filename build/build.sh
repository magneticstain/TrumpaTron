#!/bin/bash

#
# TrumpaTron Build Script
#   - express build TrumpaTron for a given server
#

APP_DIR="/opt/trumpatron/"

# create directories
echo "Creating application directory..."
mkdir $APP_DIR > /dev/null 2>&1

# run unit tests
python -m pytest build/tests/ || exit 1

# application runs
# config check/smoke test
python ./trumpatron.py -k || exit 1

echo "Build process complete!"

exit 0