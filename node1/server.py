import socket
import sqlite3
from sqlite3 import Error

def Main():
    host = "127.0.0.2";
    port = 5000;

    datas = [];

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Server: Connection from " + str(addr))
    data = conn.recv(1024).decode()
    print("DATA:", data);
    if not data:
        return
    print ("Server: recv " + str(data));
    datas.append(data.split("$")[0]);
    datas.append(data.split("$")[1]);

    try:
        condb = sqlite3.connect(datas[0]);
        print(sqlite3.version);
        cur = condb.cursor();
        cur.execute(datas[1]);
        message = "./books.sql success.$" + host + ":" +  str(port) + datas[0];
        condb.commit();
        conn.send(message.encode());
    except Error as e:
        print(e);
        message = "./books.sql failure.$" + host + ":" + str(port) + datas[0];
        conn.send(message.encode());
    finally:
        condb.close();
        conn.close();

if __name__ == '__main__':
    Main()
