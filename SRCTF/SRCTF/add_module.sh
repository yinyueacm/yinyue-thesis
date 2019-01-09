#!/bin/sh

MIGRATE_PATH=$PWD
CATEGORY=$1

cp -r ctfs/$CATEGORY $CTF_PROJECT/ctfs/
mysql -udjdb -pdjango -hlocalhost djdb < $MIGRATE_PATH/sql_scripts/djdb.sql


