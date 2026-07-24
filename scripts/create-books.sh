#!/bin/bash

echo "30+30+01::started"
mkdir books/30+30+01
chordpro "--cover=songbooks/covers/30+30+01.pdf" "--filelist=songbooks/30+30+01.list" "--output=books/30+30+01/guitar.pdf" "--config=./config/settings.json"
chordpro "--cover=songbooks/covers/30+30+01.pdf" "--filelist=songbooks/30+30+01.list" "--output=books/30+30+01/bass.pdf" "--decapo" "--config=./config/settings.json"
echo "30+30+01::completed"

# echo "wedding::started"
# chordpro "--title=Svadobné" "--filelist=songbooks/30+30+01.list" "--output=books/30+30+01.pdf" "--config=./config/settings.json"
# chordpro "--title=Svadobné" "--filelist=songbooks/30+30+01.list" "--output=books/30+30+01.bass.pdf" "--decapo" "--config=./config/settings.json"
# echo "wedding::completed"
