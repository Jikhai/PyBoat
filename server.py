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
P1wins = 0
P2wins = 0
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

    try :
       hostname=socket.gethostname()
       ipaddr=socket.gethostbyname(hostname)
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(-1)
    print("gethostbyname gave() : ",ipaddr,", the port the game runs on is : ",port)

    lesocket.listen(1)
   
#-------------------- Local variables space --------------------#
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
    
    #variables that dictate the game's status
    usrcount = 0
    isgameinit = 0
    state = 0

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
                    if isgameinit < 2 : #only two when the two players 
                        #have recieved the boat position data.
                        player1.send(pickle.dumps(boats1))
                        time.sleep(1)
                        player1.send(pickle.dumps(boats2))
                        isgameinit +=1
                        sending(player1,"Waiting for opponent...")
                elif player2 == '' :
                    player2 = established
                    player2.send(greeting + p2)
                    print("connection to player 2 established !")
                    if isgameinit < 2 : 
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
            sending(player1,"PLAY")
            text = recieve(player1,4096)
            if text == '':
                player1.close()
                player1=''
                print(" connection to player 1 lost")
                usrcount -=1
                sending(player2,"VICTORY")
                #fonction de reset
            #print(text) #debug
            x =  int(text[1])
            y =  int(text[4])
            res = main.addShot(game, x, y, 0) #returns True or False
            #print(res)
            sending(player1,str(res))
            report =(x,y,res)
            #print(report)
            sending(player2,str(report))
            time.sleep(1)
            sending(player2,"PLAY")
            text = (player2.recv(4096).decode("UTF_8"))
            if text == '':
                player2.close()
                player2=''
                print(" connection to player 2 lost")
                usrcount -=1
                sending(player1,"VICTORY")
                #fonction de reset
            #print(text) #debug
            x = int(text[1])
            y = int(text[4])
            res = main.addShot(game, x, y, 1)
            sending(player2,str(res))
            report =(x,y,res)
            #print(report)
            sending(player1,str(report))
            time.sleep(1)
        else:
            if main.gameOver(game) == 0:
                sending(player1,"VICTORY")
                P1wins +=1
                sending(player2,"DEFEAT")
                #fonction de reset
            elif main.gameOver(game) == 1:
                sending(player1,"DEFEAT")
                sending(player2,"VICTORY")
                P2wins +=1
                #fonction de reset

            ''' text=i.recv(4096).decode("UTF_8")
                if len(text) == 0 :
                    if i == player1 :
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
                    if i == player1 :'''

    else :
        lesocket.close()
        sys.exit(0)

def recieve(player,size):
    try :
        data = player.recv(size).decode("UTF_8")
    except Exception as err :
        print ("Failure ! -->", err)
        return ''
    if len(data) == 0 :
        return ''
    return data

def sending(player,data):
    try :
        player.send((data).encode("UTF_8"))
    except Exception as err :
        print ("Failure ! -->", err)
        return -1
    return 0
def reset():
  #TODO
  a=0
