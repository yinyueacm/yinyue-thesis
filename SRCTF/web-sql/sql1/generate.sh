#!/bin/bash
cd $CTF_PROJECT/ctfs/www/sql1


rm -rf for_guest/*
cp -r *.php bootstrap.min.css secdawgs.png sqlctf.sql for_guest
