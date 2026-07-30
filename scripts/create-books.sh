#!/bin/bash

echo "30+30+01::started"
mkdir -p books/30+30+01
chordpro "--cover=songbooks/covers/30+30+01.pdf" "--filelist=songbooks/30+30+01.list" "--output=books/30+30+01/30+30+01.guitar.pdf" "--config=./config/settings.json"
chordpro "--cover=songbooks/covers/30+30+01.bass.pdf" "--filelist=songbooks/30+30+01.list" "--output=books/30+30+01/30+30+01.bass.pdf" "--decapo" "--config=./config/settings.json"
echo "30+30+01::completed"

echo "wedding::started"
mkdir -p books/wedding
chordpro "--cover=songbooks/covers/wedding.pdf" "--filelist=songbooks/wedding.list" "--output=books/wedding/wedding.guitar.pdf" "--config=./config/settings.json"
chordpro "--cover=songbooks/covers/wedding.pdf" "--filelist=songbooks/wedding.list" "--output=books/wedding/wedding.bass.pdf" "--decapo" "--config=./config/settings.json"
echo "wedding::completed"

echo "masterbook:started"
mkdir -p books/masterbook
chordpro "--cover=songbooks/covers/masterbook.pdf" songs/**/*.cho "--output=books/masterbook/masterbook.guitar.pdf" "--config=./config/settings.json"
chordpro "--cover=songbooks/covers/masterbook.bass.pdf" songs/**/*.cho "--output=books/masterbook/masterbook.bass.pdf" "--decapo" "--config=./config/settings.json"
echo "masterbook:completed"
