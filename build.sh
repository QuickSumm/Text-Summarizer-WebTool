#!/usr/bin/env bash

echo "Downloading NLTK data..."
python -m nltk.downloader punkt

echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm
