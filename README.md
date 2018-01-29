# Homework 1: DDL Processing for a Parallel DBMS
* [Installation](#installation)
  * [Install Docker Containers](#install-docker-containers)
  * [Setup a Docker Container](#setup-a-docker-container)
  * [Setup Python](#setup-python)
  * [How to Install Homework 1 Program](#how-to-install-homework-1-program)
  * [How to Run Homework 1 Program](#how-to-run-homework-1-program)
* [Overview](#overview)
  * [Directory Structure](#directory-structure)
  * [File and Program Descriptions](#file-and-program-descriptions)
  * [Expected Output and Error Conditions](#expected-output-and-error-conditions)
* [Cheat Sheets](#cheat-sheets)
  * [Docker Cheat Sheet](#docker-cheat-sheet)
  * [Linux Cheat Sheet](#linux-cheat-sheet)

# Installation

## Install Docker Containers
First, download the Docker Community Edition (CE) for the Desktop from their [download page](https://www.docker.com/community-edition#/download).

Secondly, follow their instructions at their [Getting Started Page](https://docs.docker.com/get-started/).

If you want [hands-on tutorials](https://docs.docker.com/get-started/) or would like to use their [training videos and online playground](http://training.play-with-docker.com/), please feel free to do so.

## Setup a Docker Container
First, open up a terminal or command prompt window and cd to the designated Docker directory:
```
cd Desktop/Docker
```
After you're in your designated Docker directory, start your own container. In this case, I named my container "myContainer" and started it up with Ubuntu:
```
docker run -it --name=[myContainer] ubuntu
```
Since the base Ubuntu image only has the bare minimal packages installed, we will need to install some more packages:
```
apt-get -y update
apt-get -y install iputils-ping
apt-get -y install iproute
apt-get -y install dnsutils
```
You can find the ip address of your current container by doing ip a. For example, my container's ip is 172.17.0.2.:
```
ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1
    link/ipip 0.0.0.0 brd 0.0.0.0
3: ip6tnl0@NONE: <NOARP> mtu 1452 qdisc noop state DOWN group default qlen 1
    link/tunnel6 :: brd ::
6: eth0@if7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever
```
You can also ping the address of your container or other containers that you have created by using the ping:
```
ping 172.18.0.3
```
Professor Lipyeow Lim provides us with a very good demonstration of setting up a docker container and pinging:
[![OH NO SOMETHING WENT WRONG](http://img.youtube.com/vi/YHL_TaSC_hk/0.jpg)](http://www.youtube.com/watch?feature=player_embedded&v=YHL_TaSC_hk)

## Setup Python
Now that we've installed the packages we need, let's also install Python3, package installer, vim, and sqlite3:
```
apt-get -y install python3
apt-get -y install python3-pip
apt-get -y install vim
apt-get -y install sqlite3
```
Since it is not a good practice to work in root, let's create a user account:
```
adduser [username]
```
Make sure to follow the onscreen instructions!
```
su ly
cd
mkdir [directory name]
cd [directory name]
```
## How to Install Homework 1 Program
Leave the terminal or command prompt open and go to my [github page](https://github.com/saehyuns/hw1). Download the zip containing my homework 1 files and store / unzip it into the designated docker directory.

Now start up a new terminal or command prompt tab or window and go to your designated docker directory, and copy the files into your container. In my case:
```
docker cp /Users/SaeHyunSong/Desktop/Docker [Container Name]:/home/[user name]/
```
Now go back to your container and cd into the hw1 directory and voila we're all done with the installation process!

## How to Run Homework 1 Program


# Overview

## Directory Structure
The top-level directory structure contains:
```
catalog/          # Holds the sqlite3 database mycatdb and the server program.
  mycatdb         # The sqlite3 database called mycatdb.
  parDBd.py       # The server program for the catalog node.
  
node1/            # Holds the sqlite3 database mydb1 and the server program.
  mydb1           # The sqlite3 database called mydb1.
  parDBd.py       # The server program for the node1 node.
  
node2/            # Holds the sqlite3 database mydb2 and the server program.
  mydb2           # The sqlite3 database called mydb2.
  parDBd.py       # The server program for the node2 node.
  
README.md         # Contains information about installation and files.
cluster.cfg       # A configuration file that contains information about the nodes.
books.sql         # Contains a DDL command which is used to run on the node's database.
run.sh            # A shell script to run runDDL.py with two commandline arguments cluster.cfg and books.sql
runDDL.py         # Contains the main source code to parse config file and sql file and send info to the node servers.
```

## File and Program Descriptions
### Server Files
There are three server files one for each node called parDBd.py along with their own sqlite3 database:
```
catalog/          # Holds the sqlite3 database mycatdb and the server program.
  mycatdb         # The sqlite3 database called mycatdb.
  parDBd.py       # The server program for the catalog node.
  
node1/            # Holds the sqlite3 database mydb1 and the server program.
  mydb1           # The sqlite3 database called mydb1.
  parDBd.py       # The server program for the node1 node.
  
node2/            # Holds the sqlite3 database mydb2 and the server program.
  mydb2           # The sqlite3 database called mydb2.
  parDBd.py       # The server program for the node2 node.
```
The node1 and node2 directory has the same server program but different database names:
```
node1/            # Holds the sqlite3 database mydb1 and the server program.
  mydb1           # The sqlite3 database called mydb1.
  parDBd.py       # The server program for the node1 node.
  
node2/            # Holds the sqlite3 database mydb2 and the server program.
  mydb2           # The sqlite3 database called mydb2.
  parDBd.py       # The server program for the node2 node.
```
The parDBd.py program for node1/ and node2/ contains:
```
# Importing all the necessary libraries.
import socket

import sqlite3
from sqlite3 import Error

import sys
from sys import argv

# A main function that takes in two commandline arguments.
def Main(argv):
    host = argv[1];
    port = argv[2];
    #host = "127.0.0.2";
    #port = 5000;

    # Store data received into datas array.
    datas = [];

    mySocket = socket.socket()
    mySocket.bind((str(host),int(port)))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    # print ("Server: Connection from " + str(addr))
    data = conn.recv(1024).decode()
    # print("DATA:", data);
    if not data:
        return
    # print ("Server: recv " + str(data));
    datas.append(data.split("$")[0]);
    datas.append(data.split("$")[1]);

    # Connect to sqlite database in node1 directory and execute DDL command.
    try:
        condb = sqlite3.connect("../node2" + datas[0]);
        # print(sqlite3.version);
        cur = condb.cursor();
        cur.execute(datas[1]);
        message = "./books.sql success.$" + host + ":" +  str(port) + datas[0];
        condb.commit();
        conn.send(message.encode());
    # If there is an error, send a message back to client that it was a failure.
    except Error as e:
        # print(e);
        message = "./books.sql failure.$" + host + ":" + str(port) + datas[0];
        conn.send(message.encode());
    # After everything, finally close the db and the connection between client / server.
    finally:
        condb.close();
        conn.close();
# Run main function with argv parameters (commandline arguments)
Main(argv);
```
What this server program is basically doing is that it takes in two commandline arguments: IP address or hostname, and the port number. It uses those command line arguments to generate a socket with that ip address and port number. The socket will then listen for any data sent to it. Using the data it has received, it will connect to it's sqlite3 database with the data containing the database name. Execute the DDL statement that was sent along with the database name. Which then it will send a message back to the client program that it was successful or not. Then it finally closes all the connections after everything has been done. 

The catalog directory has a slightly different server program compared to the node1 and node2 servers:
```
catalog/          # Holds the sqlite3 database mycatdb and the server program.
  mycatdb         # The sqlite3 database called mycatdb.
  parDBd.py       # The server program for the catalog node.
```
The parDBd.py program for catalog/ contains: 


### Config Files
### Client Program

## Expected Output and Error Conditions

# Cheat Sheets

## Docker Cheat Sheet
Here is a simple [Docker Cheat Sheet](https://www.docker.com/sites/default/files/Docker_CheatSheet_08.09.2016_0.pdf) provided by Docker in case you're unfamiliar with the commands.

## Linux Cheat Sheet
Here is a [Linux/Unix Commands Reference](https://files.fosswire.com/2007/08/fwunixref.pdf) in case you're unfamiliar with the system as we will be using a Docker Linux Container with Ubuntu.
