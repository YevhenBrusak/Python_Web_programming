#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

host = '127.0.0.1'                           
port = 9999

serverSocket.connect((host, port))   

print("If you want to quit - Enter : 'Exit' ")
while True:
    message = input(">>> ")
    if message == "Exit" :
        serverSocket.send(message.encode('utf-8'))
        serverSocket.close()
        break
    else :
        serverSocket.send(message.encode('utf-8'))
        server_responce = serverSocket.recv(1024)
        print(server_responce.decode('utf-8'))