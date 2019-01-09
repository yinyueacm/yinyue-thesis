# SR-CTF Get_Started
Stepwise, Reusable CTF framework
By NSSLab@UGA

For detailed information, please read the `README.md`
        
1. Set up the environment
    Run the command:

    ```
    ./install.sh
    ```

2. Create Django Superuser
After successfully migrate the website, you need to create an admin account to manage django site.  

    ```
    cd $PATH/django_reuse
    python manage.py createsuperuser
    ```

    [!]Do not use superuser account to login into the reuse ctf website. It is just for admin management website.

3. Import the Sequence
    [Available Challenges](http://tunablectf.com/challenge.html)

4. Start the Server

    Navigate to the folder that contains the source code of the website  
    ```
    cd $PATH/django_reuse
    python manage.py runserver --insecure
    ```
    This command will startup the server at `localhost` and port `8000`.
    You can also start the server at different port and different ip address.
    ```
    python manage.py runserver [$ip_address]:[$port_number] --insecure
    ```