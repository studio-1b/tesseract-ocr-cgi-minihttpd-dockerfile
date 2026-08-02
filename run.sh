#!/bin/bash

docker build -t tesseractimage .
docker run --rm --name tesseractbase -v /home/bob/tesseract-cgi/img:/tmp/ocr -p8000:80 -it -d tesseractimage

curl -X POST --data-binary @img/que-es-lorem-ipsum.jpg http://localhost:8000/cgi/tesseract.cgi?que-es-lorem-ipsum.jpg
