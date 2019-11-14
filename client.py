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
    shots = []
    boats = ''
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
        data = lesocket.recv(4096)
        if len(data) ==0 :
            print("connection to server lost !")
            lesocket.close()
        else :
            try :
                data = data.decode("UTF_8")
            except Exception as err :
                #print("not a regular message :p") #debug
                data = pickle.loads(data)
                Display(data, data, shots, shots)
            print(data)
            print("--------------------------------------------------------\n")

    #TODO à déclarer les variables de mémoire de jeu
    #reception des placements de bateau et stockage dans un tableau
    #b = Boat()
    #boats = []



def Display(boats1, boats2, shots1, shots2):
    main.displayConfiguration(boats1, shots1, True)
    main.displayConfiguration(boats2, shots2, False)



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
