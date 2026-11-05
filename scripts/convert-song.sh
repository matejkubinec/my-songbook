#!/usr/bin/env bash

echo $1

set -e

# Strip the .cho extension to create the output name
output_name="${1%.cho}.pdf"

echo "Processing: $1 -> $output_name"

chordpro \
    --config=./config/guitar.json \
    --output="$output_name" \
    "$1"
