#!/bin/bash
cd $CTF_PROJECT/ctfs/www/web2


rm -rf for_guest/*
cp -r *.php bootstrap.min.css secdawgs.png sqlctf.sql pass.txt for_guest
