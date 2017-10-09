# NodeRed- IoT Starter Kit

### Run NodeRed in docker
- It is recommended that you use the following installation script [https://github.com/JoTioTech/IQRF-IoT/tree/master/install_script] for a function within the IoT Starter Kit.

- You can run  several instances of NodeRed, just need to change (name, IP address, port)
- For example:
```Bash
sudo docker run -d -p 1882:1880 --restart=always --network=isolated_nw --ip=172.25.4.2 --name redgw2 jotio/iqrf_nr_iot:latest  
```
### For editing go to yours URL/admin

- Eaxample if port mapping is set to 80:1880   [http://192.168.1.1/admin]
- Eaxample if port mapping is set to 1880:1880 [http://192.168.1.1:1880/admin]

### For login to admin
- username: admin
- password: iqrf


