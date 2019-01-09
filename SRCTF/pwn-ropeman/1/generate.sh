#!/bin/bash
cd $CTF_PROJECT/ctfs/ropeman/1
make clean

echo \#define CVAL \"AAAA\" > config.h
echo \#define BSIZE BB >> config.h

rand_cval="$((RANDOM%(9999-1000+1)+1000))"
echo $rand_cval
sed -i 's/AAAA/'$rand_cval'/' "config.h"

rand_bsize="$((RANDOM%(131060-8+1)+8))"

echo $rand_bsize
sed -i 's/BB/'$rand_bsize'/' "config.h"

make

rm -rf for_guest/*
cp -r ../ro ../rw ../README for_guest
cp ropeman for_guest/ro
