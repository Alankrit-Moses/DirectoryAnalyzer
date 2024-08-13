#!/bin/bash

# Define the file containing the package names
PACKAGE_FILE="requirements.txt"

# Check if the file exists
if [[ -f "$PACKAGE_FILE" ]]; then
    # Read the file line by line
    while IFS= read -r package || [[ -n "$package" ]]; do
        # Skip empty lines and lines starting with '#'
        if [[ -n "$package" && ! "$package" =~ ^# ]]; then
            echo "Installing $package..."
            pip install "$package"
        fi
    done < "$PACKAGE_FILE"
else
    echo "File $PACKAGE_FILE does not exist."
fi