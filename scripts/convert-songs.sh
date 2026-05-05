#!/usr/bin/env bash

find songs -name "*.cho" | grep -v "(WIP)" | while read -r song; do
    # Strip the .cho extension to create the output name
    output_name="${song%.cho}.pdf"

    chordpro \
        --transcode=scandinavian \
        --config=./config/guitar.json \
        --output="$output_name" \
        "$song"
done
