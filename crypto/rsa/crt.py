#!/usr/bin/python

from Cryptodome.Util.number import *
from Cryptodome import Random
from binascii import unhexlify
from pwn import *
import Cryptodome
import sys
import libnum
import re
import argparse
import time

#Definisanje promenjivih
rx = re.compile('\W+') 
argParser = argparse.ArgumentParser()
ctr = 1
cypherList = []
keyList = []
crib = ""

#Deklarisanje mogucih ulaznih argumenata
argParser.add_argument("-a", "--address", help="IPv4 adresa mete")
argParser.add_argument("-c", "--crib", help="Poznati deo otvorenog teksta")
argParser.add_argument("-p", "--port", type=int, help="Port mete na kome radi servis")
argParser.add_argument("-r", "--rounds", type=int, help="Broj rundi pokusavanja desifrovanja")


args = argParser.parse_args()


#Provera ispravnosti argumenata
try:    

    HOST = args.address
    
except:
    
    print("IP adressa nije uneta ili je uneta nepravilno")
    exit()

try:    

    PORT = args.port
    
except:
    
    print("Port nije unet ili je unet nepravilno")
    exit()
   
  

if(args.crib != None):
    crib = args.crib
    crib = bytearray(crib.encode())

if(args.rounds != None):
    rounds = args.rounds
else :
    rounds = 65537

try:

    s = remote(HOST, PORT)
    
except:
    
    print("IP adressa ili port su uneti nepravilno")
    exit()



while (ctr <= rounds):
    
    time.sleep(1)
    
    s.recv() #Primanje Pocetne poruke u prvoj rundi petlje i primanje sifrata i kljuca u svakoj sledecoj
    s.send(b'Y')
    message = (s.recv().decode()).split(' ') #Cuvanje sifrata i kljuca u obliku niza

    for i in range(len(message)):
        message[i] = rx.sub(' ', message[i]).strip() #Koriscenje regularnog izraza u cilju uklanjanja znakova interpunkcije iz poruke

    #Izvlacenje sifrata i kljuca iz niza, konvertovanje istih u brojeve i dodavanje na kraj listi
    try:
        cypherList.append(bytes_to_long(unhexlify(message[1])))
        keyList.append(bytes_to_long(unhexlify(message[3])))
    
    except:
        pass
    
    #Racunanje Kineske teorije ostatka i n-tog korena 
    res=libnum.solve_crt(cypherList,keyList)
    val=libnum.nroot(res,ctr)
    
    plainText = long_to_bytes(val)
        
    if (crib != ""):
        
        if (crib in plainText):
            print("\n\nResenje je sledece:")
            for i in range (len(cypherList)):  
                print(f"\nSifrat {i+1} : {cypherList[i]} \n\nJavni Kljuc {i+1} = {keyList[i]}")
            print(f"\nResimo M^e koristeci Kinesku teoriju ostatka i dobijemo: {res}")
            print(f"\nAko pretpostavimo da je e={ctr}, odradimo koren {ctr}-og stepena i dobijamo: {val}")
            print(f"\nNa kraju dobijamo pravi desifrovani tekst: {plainText.decode()}")
            s.close()
            exit() 
            
    print(f"\nDesifrovani tekst za e={ctr} je sledeci: {plainText}")

    ctr+=1
    s.send(b'Y')

s.close()
exit()    
