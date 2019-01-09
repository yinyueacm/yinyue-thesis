#!/bin/bash
cd $CTF_PROJECT/ctfs/ropeman/6

rm -rf for_guest/*
cp -r ../ro ../rw ../README for_guest
cp ropeman for_guest/ro