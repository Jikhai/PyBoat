#!/usr/bin/python3
from game import *
import main
from server import *
import pickle
import os
import sys
import string
import socket
def ClieGestion(): #all of the logic for the client side

    #---- GAME VARIABLES ----#
    boats = '' #position of boats sent at the start of the game
    hostiles = '' #position of ennemy boats
    text = '' #text sent by the server to display on screen
    shots = [] #list of shots used to display shots that have been fired
    shots2 =[]
    win = ''
    #----                ----#

    try :
        lesocket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM, 0)
    except Exception as err:
        print("Failure ! -->",err)
        sys.exit(-1)

    try :
        lesocket.connect(("localhost",7777))
    except Exception as err :
        print("Failure --> ",err)
        sys.exit(-1)

    while win == '' :
        if boats != '' and hostiles != '' : # if boat data has been set up
            Display(boats,hostiles,shots,shots2)
            print("\n----------------------\n")
        try :
            data = lesocket.recv(4096)
        except Exception as err:
            print ("Failure !  -->",err)
            sys.exit(-1)
        if len(data) ==0 :
            print("connection to server lost !\n if you were playing, that's a loss on your side.")
            lesocket.close()
        else :
            try : # if it can't be decoded then it's the data for boat positions
                text  = data.decode("UTF_8") #play
            except Exception as err :
                #print("not a regular message :p") #debug
                text = ''
                if boats== '':
                    boats = pickle.loads(data) # rebuilding the boat data from bytes
                elif hostiles == '' :
                    hostiles = pickle.loads(data) #same for ennemies
                else :
                    print("weird, you recieved unreadable data, we'll just ignore it for now\n")
            if text == "PLAY" :
                    print("TAKE AIM !")
                    x,y = fire()
                    coord = (x,y)
                    coord = str(coord)
                    lesocket.send(coord.encode())
                    result = (lesocket.recv(1024)).decode("UTF_8")
                    if result == "True" :
                        shots2.append((x, y, True))# --> shots to the other player

                    elif result == "False" :
                        shots2.append((x, y, False))# --> shots to the other player
                    print("DONE!")
            elif text == "VICTORY" :
                win = "win"
                won()

            elif text == "DEFEAT" :
                win = "loose"
                loose()

            elif text.startswith("(") : #that's a shot dataset
                print("your opponent played :")
                x = int(text[1])
                y = int(text[4])
                result = text[7:-1]
                #print(x, y, result) #debug
                if result == "True" :
                    shots.append((x, y, True))# --> shots to the other player
                elif result == "False" :
                    shots.append((x, y, False))# --> shots to the other player
            elif text !='' :
                print(text)
                text=''







def Display(boats1, boats2, shots, shots2):
    main.displayConfiguration(boats1, shots, True)
    main.displayConfiguration(boats2, shots2, False)

def fire():
    x_char = ''
    y = 0
    while x_char > 'J' or x_char < 'A' or len(x_char) > 1 :
        x_char = input ("quelle colonne ? ")
        x_char = x_char.capitalize()
    x = ord(x_char)-ord("A")+1
    while y < 1 or y > 10 :
        y = int(input ("quelle ligne ? "))
    return x,y

def won ():
    print("you win ! ending the game now.\n")

def loose():
    print("you loose ! ending the game now.\n")
