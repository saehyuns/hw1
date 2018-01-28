import socket
import sqlite3
from sqlite3 import Error

def Main():
    host = "127.0.0.1"
    port = 5000

    datas = [];

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Server: Connection from " + str(addr))
    data = conn.recv(1024).decode()
    if not data:
        return
    print ("Server: recv " + str(data));
    datap = data.split("$");
    if datap[0] == "./books.sql success.":
        try:
            con = sqlite3.connect("../catalog/mycatdb");
            cur = con.cursor();
            cur.execute("CREATE TABLE IF NOT EXISTS DTABLES(tname char(32), nodedriver char(64), nodeurl char(128), nodeuser char(16), nodepasswd char(16), partmtd int, nodeid int, partcol char(32), partparam1 char(32), partparam2 char(32));");
            cur.execute("INSERT INTO DTABLES(tname, nodedriver, nodeurl, nodeuser, nodepasswd, partmtd, nodeid, partcol, partparam1, partparam2) VALUES (" + "'" + datap[1] + "'" + ", NULL, " + "'" + datap[2] + "'" + ", NULL, NULL, NULL, 1, NULL, NULL, NULL);");
            con.commit();
            message = "catalog updated.";
            conn.send(message.encode()); 
        except Error as e:
            print(e);
        finally:
            con.close(); 
    else:
        message = "catalog not updated."
        conn.send(message.encode());

if __name__ == '__main__':
    Main()
    Main()

