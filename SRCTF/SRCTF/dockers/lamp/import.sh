#!/bin/bash
mv /app/sqlctf.sql /tmp/sqlctf.sql
c=1
while [ $c -le 5 ]
do
    mysql -uroot sqlctf < /tmp/sqlctf.sql
    (( c++ ))
done
