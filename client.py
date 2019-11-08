#!/usr/bin/python3
from main import *
#from game import *
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

    data = lesocket.recv(1500).decode("UTF_8")
    print(data)

    #TODO à déclarer les variables de mémoire de jeu
    #reception des placements de bateau et stockage dans un tableau
    #b = Boat()
    boats = []
    print("--------------------------------------------------------\n")
    for i in range(10):
        x = lesocket.recv(1024)
        boats[i] = x
        #Test print
        y = lesocket.recv(1024)
        boats[i + 1] = y
        #Test print
        i = i + 1

    for i in range(10):
        if i%2 == 0:
            print("x = "+ boats[i])
        else:
            print("y = "+ boats[i])
        print("\n")
    #for i in range(5):
    #    x = lesocket.recv(1024)
    #    b.x = x
    #    #Test print
    #    print(x)
    #    y = lesocket.recv(1024)
    #    b.y = y
    #    #Test print
    #    print(y)
    #    boats[i] = b

    while True :
        a=0
    ''' la logique grosso merdo
        affichage()
        data = lesocket.recv(2048).decode("UTF_8")
            if data = "PLAY" :
                #jouer un tir
            elif data = #format de coup joué :
                #ajouter à la liste des coups joués
            elif #code victoire ou defaite :
                changer le tableau du compte de match
            elif #information spéciale :
                 #à  voir
            else :
                #erreur ou warning'''
