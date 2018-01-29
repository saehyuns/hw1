# Import all necessary libraries. 
import socket

import sqlite3
from sqlite3 import Error

# A Main function which listens for a message from the nodes to create catalog db and update the db.
def Main():
    # Host / port initialized with constant values.
    host = "127.0.0.10"
    port = 5000

    # Messages received will be store in datas array.
    datas = [];

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    # print ("Server: Connection from " + str(addr))
    data = conn.recv(1024).decode()
    if not data:
        return
    # print ("Server: recv " + str(data));
    datap = data.split("$");
    # Connect to the mycatdb sqlite3 database and execute a create table / insert DDL command.
    try:
        con = sqlite3.connect("../catalog/mycatdb");
        cur = con.cursor();
        cur.execute("CREATE TABLE IF NOT EXISTS DTABLES(tname char(32), nodedriver char(64), nodeurl char(128), nodeuser char(16), nodepasswd char(16), partmtd int, nodeid int, partcol char(32), partparam1 char(32), partparam2 char(32));");
        cur.execute("INSERT INTO DTABLES(tname, nodedriver, nodeurl, nodeuser, nodepasswd, partmtd, nodeid, partcol, partparam1, partparam2) VALUES (" + "'" + datap[1] + "'" + ", NULL, " + "'" + datap[2] + "'" + ", NULL, NULL, NULL, 1, NULL, NULL, NULL);");
        con.commit();
        message = "catalog updated.";
        conn.send(message.encode()); 
    # If there is an error send back an error message to client.
    except Error as e:
        # print(e);
        message = e;
        conn.send(message.encode()); 
        con.close(); 
    # Finally, close all connections.
    finally:
        con.close(); 

if __name__ == '__main__':
    Main();
    Main();

