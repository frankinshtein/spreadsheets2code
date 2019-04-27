#!/usr/bin/env bash

XML=temp/data.xml
python ../google2xml/google2xml.py -s 1CX34Lyg2MDEV2TIzie-YoKhY5ZijoCFf9HmwQJePGNE -c credentials.json -d $XML
python ../xml2code/xml2code.py $XML -d temp/gdoc -p com.model.gdoc