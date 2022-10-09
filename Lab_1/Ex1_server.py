#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket 
import datetime as dt
from time import sleep

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = '127.0.0.1'                           
port = 9999                                           

serversocket.bind((host, port))                                  
serversocket.listen(5)
print('The server is waiting for connection')                                           
clientsocket, addr = serversocket.accept()      
print('Got a connection from {}'.format(addr))

while True:
    client_answer = clientsocket.recv(1024)
    print(client_answer.decode('utf-8') + " " + str(dt.datetime.now()))
    if client_answer.decode('utf-8') == "Exit" :
        clientsocket.close()
        break
    else :
        sleep(5)
        clientsocket.send(client_answer)
