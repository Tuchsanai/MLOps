#!/bin/bash

# Remove the git-lab directory if it exists
if [ -d "git-lab" ]; then
    echo "Removing git-lab directory..."
    rm -rf git-lab
    echo "Cleanup complete."
else
    echo "git-lab directory not found. Nothing to clean."
fi
