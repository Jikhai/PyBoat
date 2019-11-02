#!/usr/bin/python3

import time
import os 
import sys
import string
import select
import socket
#---- Global Variable Space ----#

#Client socket list
clientlist = []

#----                       ----#


def SockGestion():
    try :
        lesocket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM, 0)
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(-1)

    lesocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    try :
        lesocket.bind(("",7777))
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(-1)

    lesocket.listen(1)
    usrcount = 0

    notifforfeit = ("Your opponent left, or was disconnected, you win by default.\n").encode("utf_8")
    #greetingnick =("please pick a username using the command : NICK <username> you can get a list of commands with HELP\n").encode("utf_8")
    greeting =("Welcome to BattleShip !").encode("utf_8")
    while True : #tests avec nc localhost 7777

        socklist,list_a,list_b = select.select(clientlist + [lesocket],[],[])    
        for i in socklist : 
            if i == lesocket :
                established, addr = lesocket.accept()
                clientlist.append(established)
                usrcount +=1 
                print("one more user connected, total : ",usrcount) 
                established.send(greeting)      
            else :
                text=i.recv(1500)
                if len(text) == 0 :
                    i.close()
                    clientlist.remove(i)
                    usrcount -=1
                    print("one user left : ", usrcount," left")
                else :
                    #that's where the magic will happen
                    print ("data transmitted")
    else : 
        lesocket.close()
        sys.exit(0)

