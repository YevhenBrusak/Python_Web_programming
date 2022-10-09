#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from threading import Thread

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

host = '127.0.0.1'                           
port = 9999

client.connect((host, port))                               

def listen_server() :
    while True :
        
        data = client.recv(2048)
        print(data.decode("utf-8"))

def send_server() :

    listen_thread = Thread(target=listen_server)
    listen_thread.start()

    while True :
        client.send(input("").encode("utf-8"))

if __name__ == "__main__" :
    send_server()