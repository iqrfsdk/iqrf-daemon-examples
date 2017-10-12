# Node-RED

Help with simple examples very much appreciated!

## nodejs, npm and nodered on ubuntu 16.04
```Bash
sudo apt-get install nodejs-legacy
sudo npm install -g --unsafe-perm node-red node-red-admin
sudo ufw allow 1880
```

## Create service file (adjust for your user)
```Bash
sudo cat /etc/systemd/system/node-red.service

[Unit]
Description=Node-RED
After=syslog.target network.target

[Service]
ExecStart=/usr/local/bin/node-red --max-old-space-size=128 -v
Restart=on-failure
KillSignal=SIGINT

# log output to syslog as 'node-red'
SyslogIdentifier=node-red
StandardOutput=syslog

# non-root user to run as (your user)
WorkingDirectory=/home/ubuntu/
User=ubuntu
Group=ubuntu

[Install]
WantedBy=multi-user.target
```

## Enable, start and status node-red service
```Bash
sudo systemctl enable node-red
sudo systemctl start node-red
sudo systemctl status node-red
```

## MQ channel support
```Bash
sudo npm install -g --unsafe-perm node-red-contrib-ipc
sudo systemctl restart node-red
```
