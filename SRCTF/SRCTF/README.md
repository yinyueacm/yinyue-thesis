# SR-CTF 
Stepwise, Reusable CTF framework
By NSSLab@UGA
[intro website](http://tunablectf.com)

# File structures
- ctfs:  
    - Dir for challenges contents
- django_reuse:  
    - The website project written in Django
- dockers:  
    - The dockerfiles for creating required docker images
        + ubuntu_14: Modified image for ubuntu14
        + lamp: Modified image for lamp
        
# CTF-Migration(set up the environment)
This script is used to migrate the CTF Website.

In order to use this script, simplely execute:  

    ./install.sh

The script will install the django framework and all other necessary dependency.
During the running of the script, you will be asked to provide some variables(Path to directory, Mysql root password, permission to install apts and so on...)
The source code of the challenges and the website will be place in a folder you name under $HOME directory.
Also, a folder named `guest` will be created in the root directory `/guests`. This folder contains the files for website users.  
The website uses MySQL database and will create a user named `djdb` with password `django`.  

After successfully migrate the website, you have to create an admin account.  
Navigate to the folder that contains the source code of the website and execute  

    python manage.py createsuperuser
    
!Do not use superuser account to login into the reuse ctf website. It is just for admin management website.

# Usage

## Start the Server

Navigate to the folder that contains the source code of the website  

    python manage.py runserver --insecure

This command will startup the server at `localhost` and port `8000`.
You can also start the server at different port and different ip address.

    python manage.py runserver ip_address:port_number --insecure
    
> According to Django document, --insecure option is used to force serving of static files with the staticfiles app even if the DEBUG setting is False. We recommend setup Apache as a proxy to serve all static files(such as css files, static binary challenges and so on)

## Technical Specification

- site /reuse is the challenge website
- site /admin is the admin management website(where your can use the superuser account to manage reuse site)

- After a new user signed up, the admin should change the related `Guest` value `is_granted` from 0 to 1, so that the granted user account have access to all challenge related informations.

- For table `Ctf_info`:
    - `status` 0 stands for closing the level to (normal) users
    - `status` 1 stands for opening the level to userss
    
- For table `Guest`:
    - `status 2 stands for users with access to all challenges(even if the ctf status is 0)
    - status 1 stands for normal users that we tracked information in "scoreboard"
    - by default, the new created guest's status is 0, which has the same access as status 1, but cannot be seen in scoreboard information.

- 
