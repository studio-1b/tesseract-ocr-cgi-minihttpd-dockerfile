#!/bin/bash

#echo "Content-type: text/html"
echo "Content-type: text/plain"

echo "Hello: from tesseract CGI"
echo "Date: $(date)"
echo "POST-Recvd: $CONTENT_LENGTH"

NOW="$(date +%y%m%d_%H%M%S)"
FILENAME=$(mktemp /tmp/$NOW-XXXXXX)
echo "Temp: $FILENAME"
trap "rm -f $FILENAME" EXIT

EXT="tiff"
if [ "$REQUEST_METHOD" == "GET" ]; then
  DATA=$QUERY_STRING
  echo "$DATA" |base64 -d >$FILENAME
  EXT=$(identify -format "%m" $FILENAME 2>/dev/null)
elif [ "$REQUEST_METHOD" == "POST" ]; then
  head -c $CONTENT_LENGTH >$FILENAME  2>&1
  EXT=$(identify -format "%m" $FILENAME 2>/dev/null)
fi
echo "Ext: $EXT"


GROUP=$QUERY_STRING
if [ "$GROUP" == "" ] || [ "$REQUEST_METHOD" == "GET" ]; then
  GROUP=$FILENAME.tiff
fi
echo "GROUP: $GROUP"
REPL="s|$FILENAME|$GROUP|g"
echo Replace: $REPL
echo ""
ls -l $FILENAME >/dev/null
if [ $? -ne 0 ]; then
  ls -l
  exit 1
fi

# OCR
NEWNAME="$FILENAME.$EXT"
mv -v $FILENAME $NEWNAME 2>&1 >/dev/null
FILENAME=$NEWNAME
trap "rm -f $FILENAME" EXIT
echo $GROUP...
echo '--START------------------------------------------'
tesseract $FILENAME -
echo '--END--------------------------------------------'


#rm -v $FILENAME
echo done $(date)
