#!/bin/sh

cd data
rm -rf hosts
wget https://github.com/racaljk/hosts/raw/master/hosts
cd ..
data/update

# python2 bin/update.py
