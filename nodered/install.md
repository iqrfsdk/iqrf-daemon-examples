UP board - Ubuntu 16.04 

sudo apt-get install nodejs-legacy
sudo npm install -g --unsafe-perm node-red node-red-admin
sudo ufw allow 1880

sudo cat /etc/systemd/system/node-red.service

[Unit]
Description=Node-RED
After=syslog.target network.target

[Service]
ExecStart=/usr/local/bin/node-red-pi --max-old-space-size=128 -v
Restart=on-failure
KillSignal=SIGINT

# log output to syslog as 'node-red'
SyslogIdentifier=node-red
StandardOutput=syslog

# non-root user to run as
WorkingDirectory=/home/ubuntu/
User=ubuntu
Group=ubuntu

[Install]
WantedBy=multi-user.target

sudo systemctl enable node-red
sudo systemctl start node-red
sudo systemctl status node-red

sudo npm install -g --unsafe-perm node-red-contrib-ipc
sudo systemctl restart node-red
