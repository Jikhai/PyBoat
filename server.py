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


def SockGestion(): # controls the opening and closing of sockets.
    try :
        lesocket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM, 0)
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(-1)

    lesocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    port= 7777
    try :
        lesocket.bind(("",port))
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(-1)
    try :
       hostname=socket.gethostbyname("localhost")
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(-1)
    print(hostname," ",port)
    lesocket.listen(1)
    usrcount = 0
    # just a list of preset notifications to send to the clients
    notifforfeit = ("Your opponent left, or was disconnected, you win by default.\n").encode("utf_8")
    #greetingnick =("please pick a username using the command : NICK <username> you can get a list of commands with HELP\n").encode("utf_8")
    greeting =("Welcome to BattleShip !\n").encode("utf_8")
    warning =("The server is already handling a game between two players\n, closing connection now.\n").encode("utf_8")
    

    #these will be the sockets for the two players
    player1 = ''
    player2 = ''

    while True : #tests avec nc localhost 7777 > will do a local client later on

        socklist,list_a,list_b = select.select(clientlist + [lesocket],[],[])    
        for i in socklist : 
            if i == lesocket :
                established, addr = lesocket.accept()
                clientlist.append(established)
                if player1 == '' : # here we're going to check if the two players
                    player1 = established # exist, and refuse further connections
                    player1.send(greeting)
                    player1.send(("you are player 1\n").encode("UTF_8"))
                    print("connection to player 1 established !")

                elif player2 == '' :
                    player2 = established
                    player2.send(greeting)
                    player2.send(("you are player 2\n").encode("UTF_8"))
                    print("connection to player 2 established !")
                else :
                    established.send(greeting)
                    established.send(warning)
                    established.close()
                    clientlist.remove(established)
                    usrcount-=1 #because it would break the count otherwise
                usrcount +=1 
                print("one more user connected, total : ",usrcount,"\n") 
                # print(clientlist) debug purposes
               
            else : # checking if the sockets are being closed, and what the clients are sending.
                text=i.recv(1500)
                if len(text) == 0 :
                    if i == player1 :
                        player1 = ''
                        print(" connection to player 1 lost")
                    elif i == player2 :
                        player2 =''
                        print("connection to player 2 lost")
                    i.close()
                    clientlist.remove(i)
                    usrcount -=1
                    print("one user left : ", usrcount," left\n")
                else :
                    #that's where the magic will happen
                    print ("data transmitted from :", i,"\n")
                    
    else : 
        lesocket.close()
        sys.exit(0)

