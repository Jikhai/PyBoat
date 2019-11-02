#!/usr/bin/python3
from game import *

def ClientGestion():
    #TODO establish connection to the server : requires having a useable address for the server. 
    print("initializing game, setting up boats")
    boats = randomConfiguration()
