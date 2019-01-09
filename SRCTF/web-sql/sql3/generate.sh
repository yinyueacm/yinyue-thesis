#!/bin/bash
cd $CTF_PROJECT/ctfs/www/sql3

rm -rf for_guest/*
cp -r *.php *.txt bootstrap.min.css secdawgs.png sqlctf.sql for_guest
