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
    strikes = 0
    strikes2 = 0
    wins = 0
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

    while True :
        if boats != '' and hostiles != '' : # if boat data has been set up
            Display(boats,hostiles,shots,shots2)
            print( "you hit ",strikes," time(s)")
            print("your opponent hit ", strikes2," times")
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
                    if result == "True" : # whever it hit or not
                        shots2.append((x, y, True))
                        strikes +=1
                    elif result == "False" :
                        shots2.append((x, y, False))
                    print("DONE!")
            elif text == "VICTORY" :
                boats,hostiles,shots,shots2,strikes,strikes2,wins = won(wins)

            elif text == "DEFEAT" :
                boats,hostiles,shots,shots2,strikes,strikes2 =  lost(wins)

            elif text.startswith("(") : #that's a shot dataset
                print("your opponent played :")
                x = int(text[1])
                y = int(text[4])
                result = text[7:-1]
                #print(x, y, result) #debug
                if result == "True" :
                    shots.append((x, y, True))
                    print("!You got Hit!")
                    strikes2 +=1
                elif result == "False" :
                    shots.append((x, y, False))
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
        x_char = input ("Pick a column (use a letter): ")
        x_char = x_char.capitalize()
    x = ord(x_char)-ord("A")+1
    while y < 1 or y > 10 :
        y = int(input ("Pick a lign (use a number): "))
    return x,y

def won(wins):
    print("you won ! ending the game now.\n")
    wins +=1 
    print("you've won ",wins," time(s) so far !")
    print("readying new game !\n")
    return '','',[],[],0,0,wins #boatlists, shots, hitcounts, wincount

def lost(wins):
    print("you lost ! ending the game now.\n")
    print("you've won ",wins," time(s) so far !")
    print("readying new game !\n")
    return '','',[],[],0,0 #boatlists, shots, hitcounts
