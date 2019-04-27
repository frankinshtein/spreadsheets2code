python ../google2xml/google2xml.py -s 1CX34Lyg2MDEV2TIzie-YoKhY5ZijoCFf9HmwQJePGNE -c credentials.json -d temp/data.xml
python ../xml2code/xml2code.py temp/data.xml -d temp/gdoc -p com.model.gdoc