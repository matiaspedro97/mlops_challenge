## Install git and update yum

```
sudo yum update

sudo install git
```
---------
# SETUP
### 1. Clone the project from github

```
git clone https://github.com/matiaspedro97/mlops_challenge.git
```

### 2. Run the setup_envs.sh file to create the environments (the file is inside the project folder)
```bash
bash setup_envs.sh
```

The file content is the following:
```bash
#!/bin/bash

python3 -m virtualenv -p /usr/bin/python3.7 .pipenv-dev &&

python3 -m virtualenv -p /usr/bin/python3.7 .pipenv-prod &&

. .pipenv-dev/bin/activate &&

pip install -r requirements/requirements-dev.txt &&

deactivate &&

. .pipenv-prod/bin/activate &&

pip install -r requirements/requirements-prod.txt

```

P.S.: In case some command has been killed, run the remaining by hand to 
ensure all the packages are installed. This is really important to get it totally reproducible.

### 3. Activate the production environment.

```bash
. .pipenv-prod/bin/activate

```

### 4. Try to run the API script.

```bash
python3 -m uvicorn src.api.api:app --workers 4
```
P.S.: In case it works, the message should be the following.

```bash
INFO:     Started server process [16466]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

```


### 5. At this point it's only running locally, so the API is still not exposed through an external URL.
To switch the visibility of the API, we have to follow a few steps

### 5.1 Install "nginx" (a proxy server that will help us expose our API publicly)

```bash
sudo yum install nginx
```

Then we need to create a file to nginx the server and the port it should refer to.
```bash
mkdir /etc/nginx/sites-enabled/
nano /etc/nginx/sites-enabled/fastapi
```

I chose to name my file as "fastapi". Inside, we should insert the following content:
```bash
server {
        listen 5000;
        server_name 54.171.118.44;
        location / {
                proxy_pass http://127.0.0.1:8000;
                }
}
```

Where the "listen" is the port your API should be exposed through (on your EC2-AWS instance).
In my case, I enabled the 5000 port from the public IP 54.171.118.44. 
The port you defined upon the instance configuration should match the port to listen from in this file.

P.S.: Note that every time you restart the instance you are running, the IP may be changed, 
and you should account for that.

### 5.2 Restart the nginx service
```bash
sudo service nginx restart
```

### 5.3 Tell the nginx file to include all the virtual hosts that are settled on the "/etc/nginx/sites-enabled/ directory.
Open the nginx.conf file for writing
```bash
nano /etc/nginx/nginx.conf

```
Add the following include command:
```bash
include /etc/nginx/sites-enabled/*;
```
right below the "# Load modular configuration files....", inside the http {} clause.

P.S. Note that you should have elevated permissions to change configuration files.
Type 'sudo su' before opening the file with "nano" or "vim" and it should work fine.


### 6. The next step consists of trying to run the API script, and see whether it is working or not.
```bash
cd /home/ec2-user/mlops_challenge/
python3 -m uvicorn src.api.api:app
```
And hope it works

---------------------------------------
# PLUS

### 7. To run the API as a background service, you should create a .service file, and place it
in the /etc/systemd/system/ directory. I called it "fastapi.service".

```bash
nano /etc/systemd/system/fastapi.service
```

Now insert the following content:

```bash
[Unit]
Description=Unicorn instance to serve MLOPS challenge API
After=network.target

[Service]
User=ec2-user
Group=nginx
WorkingDirectory=/home/ec2-user/mlops_challenge
Environment="PATH=/home/ec2-user/mlops_challenge/.pipenv-prod/bin"
ExecStart=/home/ec2-user/mlops_challenge/.pipenv-prod/bin/uvicorn src.api.api:app --workers 4

[Install]
WantedBy=multi-user.target
```

P.S. Note that you should have elevated permissions to change configuration files.
Type 'sudo su' before opening the file with "nano" or "vim" and it should work fine.
P.S.*: You should customize this file according to the field names you defined.

### 8. Finnally, we just need to run the api as a background service

```bash
sudo systemctl start fastapi.service
```

Check if the service is running by doing:
```bash
systemctl --type=service --state=running
```

In case it actually shows up in the list of services running on the EC2-AWS VM instance, 
then you're done. The API is running and you can shutdown your terminal without concerns.

-------
# Try it out
Access the following link and check how does the API look like

[KeyStroke API](http://54.171.118.44:5000/docs)
