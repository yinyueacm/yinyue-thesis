#!/bin/bash

# Installations
# 1. Python
# 2. MySQL
# 3. Django
# 4. ctf challenges folder
# 5. web source
# 6. database structure
# 7. Environment Settings


MIGRATE_PATH=$PWD


# Get env variable ready
echo "Please Enter Your Project Folder Name"
echo "All of the Files will be store at ~/PROJECT_FOLDER_NAME"

read FOLDER_NAME

echo "All Your Files Will Be Store at $HOME/$FOLDER_NAME"

cd $HOME && mkdir $FOLDER_NAME

CTF_PATH=$HOME/$FOLDER_NAME

echo "Please specify the domain name or ip of your server"
read S_DOMAIN

if [ -f $HOME/.zshrc ]; then
    echo "export CTF_PROJECT=$CTF_PATH" >> $HOME/.zshrc
    echo "export S_DOMAIN=$S_DOMAIN" >> $HOME/.zshrc
    source $HOME/.zshrc
fi

echo "export CTF_PROJECT=$CTF_PATH" >> $HOME/.bashrc
echo "export S_DOMAIN=$S_DOMAIN" >> $HOME/.bashrc
source $HOME/.bashrc
export "CTF_PROJECT=$CTF_PATH"

sudo apt-get update
# Install Python 2.7 and necessary tools
sudo apt-get install python2.7 python-setuptools mysql-server-5.5 python-mysqldb python-dev libjpeg8-dev python-pip g++-multilib

# Upgrade pip
sudo pip install --upgrage pip

# Install Django
sudo pip install Django
sudo pip install django-allauth
sudo pip install Pillow

# Create a database user for Django
echo "Please provide your mysql root password"
read -s MYSQL_PSWD

PASS="django"
USERNAME="djdb"

mysql -uroot -p$MYSQL_PSWD <<MYSQL_SCRIPT
CREATE DATABASE $USERNAME;
CREATE USER '$USERNAME'@'localhost' IDENTIFIED BY '$PASS';
GRANT ALL PRIVILEGES ON $USERNAME.* TO '$USERNAME'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

echo "MySQL user created!"
echo "Username: $USERNAME"
echo "Password: $PASS"

# unzip the webpage source and challenge source
cd $MIGRATE_PATH
#tar -xvf ctfs.tar --directory $CTF_PATH
#tar -xvf django_reuse.tar --directory $CTF_PATH
cp -r ctfs $CTF_PATH
cp -r django_reuse $CTF_PATH

# set up the database schema
cd $CTF_PATH/django_reuse
python manage.py makemigrations reuse
python manage.py sqlmigrate reuse 0008
python manage.py migrate

# container pswd_generator
cd $MIGRATE_PATH
python pswd_generator.py

# import data from current production site, remember to remove our own user data
#comment out for temp
mysql -udjdb -pdjango -hlocalhost djdb < $MIGRATE_PATH/sql_scripts/base.sql

# install docker
sudo apt-get install apt-transport-https ca-certificates
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install docker-engine
sudo service docker start
sudo groupadd docker
sudo usermod -aG docker $USER
sudo service docker restart

#build docker image
cd $MIGRATE_PATH/dockers/ubuntu_14
sudo docker build -t ctf14 .

cd $MIGRATE_PATH/dockers/lamp
sudo docker build -t mylamp .

# create a guest folder at / and change ownership
cd / && sudo mkdir /guests
sudo chown $USER:$USER -R guests

echo "Installation Complete, Please Log out and log back in to enable docker"
