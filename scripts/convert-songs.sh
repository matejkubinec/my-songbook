#!/usr/bin/env bash

find songs -name "*.cho" | grep -v "(WIP)" | while read -r song; do
    # Strip the .cho extension to create the output name
    output_name="${song%.cho}.pdf"

    echo "Processing: $song -> $output_name"

    chordpro \
        --config=./config/guitar.json \
        --output="$output_name" \
        "$song"
done
