#!/usr/bin/env bash

if [ ! -d "songs" ]; then
  echo "Error: Directory 'songs' not found."
  exit 1
fi

find songs -type f -name "*.pdf" -print0 | while IFS= read -r -d '' song; do

  PAGES=$(mdls -name kMDItemNumberOfPages -raw "$song")

  # Only report if it's a valid integer AND greater than 1
  if [[ "$PAGES" =~ ^[0-9]+$ ]] && [ "$PAGES" -gt 1 ]; then
    echo "$song: $PAGES pages"
  fi

done