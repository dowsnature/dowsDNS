#!/bin/sh

cd data
make
wget https://github.com/racaljk/hosts/raw/master/hosts
cd ..

data/update
python2 bin/dns.py
