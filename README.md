# NetworkArchitecture_msgbroker_research
All Python package requirements are listed in the requirements.txt file


# Setting up the Network:
To access the rabbitmq dashboard webserver from a local machine, needed to set up a http proxy through the firewall.

To be able to send msgs using amqp protocol, rabbitmq is based on TCP so we set up a TCP proxy to allow messages to go through.

To achieve this we used the tool nginx:https://nginx.org/en/.

In order to setup a TCP proxy for rabbitmq, we followed this guide loosely:
https://medium.com/@giorgos.dyrrahitis/configuring-an-nginx-tcp-proxy-for-my-rabbitmq-cluster-under-10-minutes-a0731ec6bfaf


The module we are interested in is the nginx stream module: https://nginx.org/en/docs/stream/ngx_stream_core_module.html

## Setting up the Virtual Machines:
The choice between using a cloud service such as AWS or running local VMs was considered, ultimately we decided to run local VMs as there was more customizability, it was free, and we would not have to worry about restrictions. 

We constructed three separate VMs in our model, all running Ubuntu Server. 

We chose Ubuntu server as it is open source, and commonly used. There are lots of tools that are compatible, and open source that can be used alongside it. They are also relatively light weight, and since we are running these machines locally, there are computing constraints in terms of power and size, however Ubuntu offers enough features out of the bag that we don’t have to dedicate many hours to configuring the setup of each machine. 

https://ubuntu.com/server


## Setting up the tunnel: 
The tool used to setup the tunnel was OpenVPN.
### OPENVPN:
OpenVPN is a full-featured SSL VPN which implements OSI layer 2 or 3 secure network extension using the industry standard SSL/TLS protocol, supports flexible client authentication methods based on certificates, smart cards, and/or username/password credentials, and allows user or group-specific access control policies using firewall rules applied to the VPN virtual interface. 

OpenVPN 2.0 expands on the capabilities of OpenVPN 1.x by offering a scalable client/server mode, allowing multiple clients to connect to a single OpenVPN server process over a single TCP or UDP port.

Source: https://openvpn.net/community-resources/how-to/

This suited our needs for creating a network tunnel. 

Upon start up, first a command is used to route the proxy through the tunnel: 
route -n add -net 192.168.123.0/24 10.8.0.1


Next the tunnel is created with the command: 
sudo openvpn --config client.ovpn   	

## Setting up the proxy server:

### NGINX:
 nginx ("engine x") is an HTTP web server, reverse proxy, content cache, load balancer, TCP/UDP proxy server, and mail proxy server. Originally written by Igor Sysoev and distributed under the 2-clause BSD License.

Known for flexibility and high performance with low resource utilization, nginx is:

	the world's most popular web server [Netcraft];
	consistently one of the most popular Docker images [DataDog];
	powering multiple Ingress Controllers for Kubernetes, including our own.


https://nginx.org/en/

In our model we used nginx as  TCP proxy, to funnel traffic heading in and out of the rabbitmq-server. 

#### Installing nginx: 
sudo apt-get update
sudo apt-get install nginx
adminy@proxy:~$ nginx -v
nginx version: nginx/1.24.0 (Ubuntu)



#### Configuring the nginx proxy: 
To configure the nginx proxy we need to edit:
/etc/nginx/nginx.conf


#### The settings we used are as follows: 
load_module modules/ngx_stream_module.so;
events {}

stream {
    	# List of upstream AMQP connections
    	upstream stream_amqp {
            	least_conn;
            	server webserver.norbazad.ron.com:5672;
    	}

    	# AMQP definition
    	server {
            	listen 5672; # the port to listen on this server
            	proxy_pass stream_amqp; # forward traffic to this upstream group
            	proxy_timeout 3s;
            	proxy_connect_timeout 3s;
    	}

}


#### Note:
Where webserver.norbazad.ron.com is the location of where the rabbitmq server sits, 5672 is the default port used for rabbitmq. 
Next, reload:
nginx -s reload


### SQUID:
Squid is a caching proxy for the Web supporting HTTP, HTTPS, FTP, and more. It reduces bandwidth and improves response times by caching and reusing frequently-requested web pages. Squid has extensive access controls and makes a great server accelerator. It runs on most available operating systems, including Windows and is licensed under the GNU GPL.

https://www.squid-cache.org/

Whilst squid has a focus on caching to improve content delivery times, we are implementing it to be used as a HTTP proxy for the webserver. When we access the rabbitmq-server webpage from our local machine (remote to the server), the data passes through squid. 


### FIREWALLD: 
Firewalld provides a dynamically managed firewall with support for network/firewall zones that define the trust level of network connections or interfaces. It has support for IPv4, IPv6 firewall settings, ethernet bridges and IP sets. There is a separation of runtime and permanent configuration options. It also provides an interface for services or applications to add firewall rules directly.
https://firewalld.org/ 

Firewalld is a simple service that is easy to setup, configure, and log errors. Utilising firewalld we created a demilitarised zone (DMZ) between the proxy and VPN router. DMZ’s are common network structures utilised in organisations to protect an internal LAN from outside traffic. 


### PROXY SETTINGS TO VIEW RABBITMQ HTTP WEB CONSOLE:
- Manual proxy configuration:
- HTTP Proxy: 192.168.123.233:3128

### PROXY SETTINGS TO VIEW ACTIVEMQ HTTP WEB CONSOLE:
- Manual proxy configuration:
- HTTP Proxy: 192.168.123.233:8161



### ACTIVEMQ SETUP:

Activemq  6.1.3: 
Installed JDK v17
Installed Maven
Couple tricky things with choosing the right JDK run time… also used java V17…just pp installing java will auto download v11


Attempt to use Python AMQP library: 
Connection attempt from non AMQP v1.0 client. AMQP,0,0,9,1

^^ what this means is that the msgs we send using the python amqp library are still using 0.9.1 protocol, which isnt compatible with V1, which the activemq server is running. 

For this reason, using Apache Qpid 