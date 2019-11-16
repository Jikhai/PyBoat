#!/usr/bin/python3
import game
import main
import time
import os
import sys
import string
import select
import socket
import pickle

#---- Global Variable Space ----#

#Client socket list
clientlist = []
#----                       ----#


def SockGestion(): # controls the opening and closing of sockets and game logic
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

    '''try :
       hostname=socket.gethostbyname("localhost")
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(-1)
    print(hostname," ",port)'''

    lesocket.listen(1)
    usrcount = 0
#-------------------- Local variables space --------------------#
    P1wins = 0
    P2wins = 0
    # just a list of preset notifications to send to the clients
    notifforfeit = ("Your opponent left, or was disconnected, you win by default.\n").encode("utf_8")
    #greetingnick =("please pick a username using the command : NICK <username> you can get a list of commands with HELP\n").encode("utf_8")
    greeting =("Welcome to BattleShip !\n").encode("utf_8")
    p2 =("you are player 2\n").encode("UTF_8")
    p1 =("you are player 1\n").encode("UTF_8")
    warning =("The server is already handling a game between two players\n, closing connection now.\n").encode("utf_8")

    #the initialisation of the game
    boats1 = main.randomConfiguration()
    boats2 = main.randomConfiguration()
    game = main.Game(boats1, boats2)
    #these will be the sockets for the two players
    player1 = ''
    player2 = ''
    isgameinit = 0
#-------------------                        --------------------#
    while True : #tests avec nc localhost 7777 > will do a local client later on

        socklist,list_a,list_b = select.select(clientlist + [lesocket],[],[],1)
        for i in socklist :
            if i == lesocket :
                established, addr = lesocket.accept()
                clientlist.append(established)
                if player1 == '' : # here we're going to check if the two players
                    player1 = established # exist, and refuse further connections
                    player1.send(greeting + p1)
                    print("connection to player 1 established !")
                    if isgameinit < 2 : #only two when the two players have recieved the boat position data.
                        player1.send(pickle.dumps(boats1))
                        time.sleep(1)
                        player1.send(pickle.dumps(boats2))
                        isgameinit +=1
                elif player2 == '' :
                    player2 = established
                    player2.send(greeting + p2)
                    print("connection to player 2 established !")
                    if isgameinit < 2 : #only two when the two players have recieved the boat position data.
                        player2.send(pickle.dumps(boats2))
                        time.sleep(1)
                        player2.send(pickle.dumps(boats1))
                        isgameinit +=1
                else :
                    established.send(greeting)
                    established.send(warning)
                    established.close()
                    clientlist.remove(established)
                    usrcount-=1 #because it would break the count otherwise
                usrcount +=1
                print("one more user connected, total : ",usrcount,"\n")
                #print(clientlist) #debug purposes

        if isgameinit == 2 and main.gameOver(game) == -1 :
            print("start of a turn !")
            res= ''
            report=''
            player1.send(("PLAY").encode("UTF_8"))
            text = (player1.recv(4096).decode("UTF_8"))
            #print(text) #debug
            x =  int(text[1])
            y =  int(text[4])
            res = main.addShot(game, x, y, 0) #retourne True ou False
            #envoyer un tuple qui contient True/false et les coordonnéesà P2 et à P1uniquement si c'est un nouveau tir (appelle isanewshot et isastrike)
            #print(res)
            player1.send(str(res).encode())
            report =(x,y,res)
            #print(report)
            player2.send(str(report).encode())
            time.sleep(1)
            player2.send(("PLAY").encode("UTF_8"))
            text = (player2.recv(4096).decode("UTF_8"))
            #print(text) #debug
            x = int(text[1])
            y = int(text[4])
            res = main.addShot(game, x, y, 1)
            player2.send(str(res).encode("UTF_8"))
            report =(x,y,res)
            #print(report)
            player1.send(str(report).encode())
            time.sleep(1)
        else:
            if main.gameOver(game) == 0:
                player1.send(("VICTORY").encode("UTF_8"))
                player2.send(("DEFEAT").encode("UTF_8"))
                #fonction de reset
            elif main.gameOver(game) == 1:
                player2.send(("VICTORY").encode("UTF_8"))
                player1.send(("DEFEAT").encode("UTF_8"))
                #fonction de reset

            ''' text=i.recv(4096).decode("UTF_8")
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
                    #print ("data transmitted from :", i,"\n")
                    #print(text)
                    if i == player1 :
                        player1.send(("PLAY").encode("UTF_8"))
                        #i.recv() (positions x et y)
                        #game.addShot(game, x, y, 0)#0 -> player 1 (test avec fonction de game)
                        #player2.send() position x y pour shots
                        #meme chose pour player 2 sauf que 0 -> 1 et send to player1

                    logique de comm avec le client
                    -> envoi des position bateau
                    ->envoi demande input
                    -> envoi résultat aux deux
                    -> envoi à l'autre joueur puis retour du résultat aux deux
                    -> envoi des messages type victoire défaite
                    '''

    else :
        lesocket.close()
        sys.exit(0)
