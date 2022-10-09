#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket 
import threading                                       

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = '127.0.0.1'                           
port = 9999                                           

server.bind((host, port))                                  

server.listen(5)
print('The server is waiting for connection') 

users = []  

def send_all(data,user_name):
    for user in users:
        if user != user_name :            
            user.send(data)

def listen_user(user):
    print("Listening user")
    while True :
        data = user.recv(2048)
        print(f"User sent {data}")
        send_all(data,user)
                

def start_server():
    while True:       
        user_socket , address = server.accept()
        print(f"User <{address[0]}> connected!")       
        users.append(user_socket)
        listen_accepted_user = threading.Thread(
            target=listen_user,
            args=(user_socket,)
        )
        listen_accepted_user.start()

if __name__ == "__main__" :
    start_server()
