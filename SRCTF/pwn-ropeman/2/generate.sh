#!/bin/bash
cd $CTF_PROJECT/ctfs/ropeman/2
make clean

echo \#define BUF_SIZE BS > config.h

rand_bsize="$((RANDOM%(8370000-1+1)+1))"

echo $rand_bsize
sed -i 's/BS/'$rand_bsize'/' "config.h"

make

rm -rf for_guest/*
cp -r ../ro ../rw ../README for_guest
cp ropeman for_guest/ro
