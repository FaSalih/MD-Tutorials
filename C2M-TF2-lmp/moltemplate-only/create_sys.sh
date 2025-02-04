#!/bin/bash

# Copy component lt files into local directory
cp ../creating-mol-lt-files/*.lt .

# Run moltemplate
moltemplate.sh  system.lt

