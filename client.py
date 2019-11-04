#!/usr/bin/python3
from game import *
from main import *
from server import *
import os
import sys
import string
import socket
def ClieGestion():

    #TODO establish connection to the server : requires having a useable address for the server.
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

    data = lesocket.recv(2048).decode("UTF_8")
    print(data)
    #TODO : Contrôl the socket properly -> send, AND recieve data without breaking stuff, current code can establish a connection but this is not enough.

    #displayGame(game, data) #the display is related to the recieved data
    #this should be handled by the server.
    #print("initializing game, setting up boats")
    #boats = randomConfiguration()
