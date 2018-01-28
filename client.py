#!/usr/bin/python3
import socket
#Hello 
def Main():
        host = '127.0.0.2'
        port = 5000
         
        mySocket = socket.socket()
        mySocket.connect((host,port))
        
        ddlfile = open("books.sql", "r")
        ddl = ddlfile.readline()
        message = "Name of the file I'm reading from: " + ddl
        ddlfile.close()
        print ('Client: send ' + str(message))
        mySocket.send(message.encode())

        data = mySocket.recv(1024).decode()
        print ('Client: recv ' + str(data))
        mySocket.close()
 
if __name__ == '__main__':
    Main()
