import socket

import sqlite3
from sqlite3 import Error

import sys
from sys import argv

def runDDL(argv):
    data = [];
    configFile = open(argv[1], "r");
    data = configFile.read().strip().replace("\n",";").split(';');
    configFile.close();

    data = list(filter(('').__ne__, data));
    ddlCommands = [];
    ddlFile = open(argv[2], "r");
    ddlCommands= ddlFile.read().strip().replace("\n","").split(';');
    ddlFile.close();

    url = '';
    hostname = '';
    port = '';
    db = '';
    numnodes = 0;
    nodes = [];

    for d in data:
        if d.strip():
            temp = d.strip().split("=");
            if temp[0].find("catalog") > -1:
                if temp[0].find("hostname") > -1:
                    url = temp[1];
                    hostname = temp[1].split("/")[0].split(":")[0];
                    port = temp[1].split("/")[0].split(":")[1];
                    db = temp[1].split("/")[1];
                    nodes.append(Node(url, hostname, port, db));
            if temp[0].find("node") > -1:
                if temp[0].find("hostname") > -1:
                    url = temp[1];
                    hostname = temp[1].split("/")[0].split(":")[0];
                    port = temp[1].split("/")[0].split(":")[1];
                    db = temp[1].split("/")[1];
                    nodes.append(Node(url, hostname, port, db));

    numnodes = len(nodes);
    tablename = ddlCommands[0].split("(")[0].split(" ")[2];
    message = nodes[1].url.split("/", 1)[1];

    x = 1;
    while(x < numnodes):
        message = nodes[x].url.split("/", 1)[1];
        message = "/" + message + "$" + ddlCommands[0];
        mySocket = socket.socket();
        mySocket.connect((nodes[x].hostname, int(nodes[x].port)));
        mySocket.send(message.encode())
        received = mySocket.recv(1024).decode();
        receivedp = received.split("$");
        mySocket.close();
        if receivedp[0] == "./books.sql success.":
            print("[" + receivedp[1] + "]: " + receivedp[0]);
            message2 = receivedp[0] + "$" + tablename + "$" + nodes[x].url;
            mySocket2 = socket.socket();
            mySocket2.connect((nodes[0].hostname, int(nodes[0].port)));
            mySocket2.send(message2.encode());
            received2 = mySocket2.recv(1024).decode();
            if received2 == "catalog updated.": 
                print("[" + nodes[0].url + "]: " + received2);
            else:  
                print("[" + nodes[0].url + "]: " + received2);
        x += 1;
        mySocket2.close();

class Node:
    def __init__(self, url, hostname, port, db):
        self.url = url;
        self.hostname = hostname;
        self.port = port;
        self.db = db;
    def displayNode(self):
        print("URL:", self.url, "HOSTNAME:", self.hostname, "PORT:", self.port, "DB:", self.db);

runDDL(argv);
