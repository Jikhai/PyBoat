#!/usr/bin/python3

from game import *
from server import *
from client import *
import  random
import time
import os
import sys
import string
import select
import socket
#---- Global Variable Space ----#
# NB : Global variables from other files also get imported
#----                       ----#

""" generate a random valid configuration """
def randomConfiguration():
    boats = [];
    while not isValidConfiguration(boats):
        boats=[]
        for i in range(5):
            x = random.randint(1,10)
            y = random.randint(1,10)
            isHorizontal = random.randint(0,1) == 0
            boats = boats + [Boat(x,y,LENGTHS_REQUIRED[i],isHorizontal)]
    return boats

    

def displayConfiguration(boats, shots=[], showBoats=True):
    Matrix = [[" " for x in range(WIDTH+1)] for y in range(WIDTH+1)]
    for i  in range(1,WIDTH+1):
        Matrix[i][0] = chr(ord("A")+i-1)
        Matrix[0][i] = i

    if showBoats:
        for i in range(NB_BOATS):
            b = boats[i]
            (w,h) = boat2rec(b)
            for dx in range(w):
                for dy in range(h):
                    Matrix[b.x+dx][b.y+dy] = str(i)

    for (x,y,stike) in shots:
        if stike:
            Matrix[x][y] = "X"
        else:
            Matrix[x][y] = "O"


    for y in range(0, WIDTH+1):
        if y == 0:
            l = "  "
        else:
            l = str(y)
            if y < 10:
                l = l + " "
        for x in range(1,WIDTH+1):
            l = l + str(Matrix[x][y]) + " "
        print(l)

""" display the game viewer by the player"""
def displayGame(game, player):
    otherPlayer = (player+1)%2
    displayConfiguration(game.boats[player], game.shots[otherPlayer], showBoats=True)
    displayConfiguration([], game.shots[player], showBoats=False)



""" Play a new random shot """
def randomNewShot(shots):
    (x,y) = (random.randint(1,10), random.randint(1,10))
    while not isANewShot(x,y,shots):
        (x,y) = (random.randint(1,10), random.randint(1,10))
    return (x,y)

def main():
    #what are we going to do today ? 
    if len(sys.argv) < 2 :
        print ("Now Running as Server ...\n\n")
        #Run server-side code here
        SockGestion()
    else: 
        if len(sys.argv) > 2 :
            print ("too many arguments, try -h, or --help")
            sys.exit(-1)
            # you dun goofed
        else :
            if sys.argv[1] == "-h" or sys.argv[1] == "--help" :
                helpmsg() 
                # nothing more to do here.
            else : 
                arg = (sys.argv[1]).split(":") #argument control
                try :
                    address = arg[0]
                    port = int(arg[1])
                except Exception as err:
                    helpmsg()
                    sys.exit(-1)
                
                print ("now running as Player ...\n\n")
                #Run player-side code here
                ClieGestion(address,port)

def helpmsg():
    print ("usage :\nmain.py <no argument> : run in server mode (note only one at a time)\nmain.py <ipadress:port> : run in client mode (only two at a time)\n-h or --help for this message\n")


if __name__ == "__main__" :
    main()
