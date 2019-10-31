#!/usr/bin/python3

from game import *
import  random
import time
import sys
import socket
import select

if len(sys.argv) == 1:
    s =  socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',1111))
    s.listen(1)
    l = [s]
    currentPlayer = 0
    print("")
    print("The server is waiting for players...\n")
    while True:
        (l1,a,b) = select.select(l,[],[])
        for i in l1:
            if i == s:
                if len(l) == 1:
                    client_1,addr = s.accept()
                    l.append(client_1)
                    client_1.send(b"Welcome, you're the first player!")
                    print("First PLayer connected...\n")
                else:
                    if len(l) == 2:
                        client_2,addr = s.accept()
                        l.append(client_2)
                        client_2.send(b"Welcome, you're the seconde the seconde player!\nAnd the game beggin!")
                        print("Seconde player connected")
            else:
                if i == client_1:
                    currentPlayer = 0
                else:
                    currentPlayer = 1
