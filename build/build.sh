#!/bin/bash

#
# TrumpaTron Build Script
#   - express build TrumpaTron for a given server
#

# run unit tests
python -m pytest build/tests/ || exit 1

# application runs
# config check/smoke test
python ./trumpatron.py -c conf/ro.cfg -t || exit 1

echo "Build process complete!"

exit 0