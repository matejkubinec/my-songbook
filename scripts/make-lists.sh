#!/bin/bash

# Ensure the script stops if a command fails (optional, uncomment if wanted)
# set -e

# Loop through all .txt files in the lists directory
for filelist in lists/*.txt; do
    # Check if any files actually match to prevent running on literal 'lists/*.txt'
    [ -e "$filelist" ] || continue

    # Get the file name without the extension, then append .pdf
    output="${filelist%.txt}.pdf"
    output_bass="${filelist%.txt}.bass.pdf"

    echo "Processing: $filelist -> $output"

    chordpro "--filelist=$filelist" "--output=$output" "--config=./config/settings.json"

    chordpro "--filelist=$filelist" "--output=$output_bass" "--decapo" "--config=./config/settings.json"
done