# -*- coding: utf-8 -*-
"""
https://uiandwe.tistory.com/1245
"""
import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'hello, world')
    data = s.recv(1024)
    
print('received', repr(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'2nd, world')
    data = s.recv(1024)

print('received', repr(data))
