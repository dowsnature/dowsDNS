#!/bin/sh

cd data
make
cd ..

python2 bin/dns.py
