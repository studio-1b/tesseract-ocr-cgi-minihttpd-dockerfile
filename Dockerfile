FROM alpine:latest

WORKDIR /root
USER root

# install bash
RUN apk add --no-cache bash

# install tesseract
RUN apk update && apk add --no-cache tesseract-ocr imagemagick curl
RUN curl -O https://raw.githubusercontent.com/tesseract-ocr/tessdata/refs/heads/main/eng.traineddata && mv eng.traineddata /usr/share/tessdata/
RUN mkdir /tmp/ocr  && chmod 666 /tmp/ocr
WORKDIR /tmp
VOLUME /tmp/ocr

# install mini-httpd
RUN apk update && apk add --no-cache mini_httpd
RUN mkdir /var/www/cgi
COPY tesseract.cgi /var/www/cgi/tesseract.cgi

#CMD ["bash"]
#CMD ["snort3/bin/snort", "-A", "cmg", "-c", "snort3/etc/snort/snort.lua", "--pcap-dir", "/tmp/pcap"]
CMD ["mini_httpd", "-p", "80", "-d", "/var/www", "-c", "cgi/*", "-D"]
