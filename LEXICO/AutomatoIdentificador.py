# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 2019

@author: Antonio Raian e Diogo Lima
"""
import string
LETRAS = list(string.ascii_letters)
NUMEROS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']

def automato_identificador(palavra):
    i = 0
    for carac in palavra:
        if(i==0 and (carac in LETRAS)):
            i+=1
        elif carac in LETRAS or carac in NUMEROS:
            i+=1
        else:
            return "ERR_IDE " + palavra

    cont=0
    if palavra=="principal":
        cont=1
    elif palavra=="inteiro":
        cont=1

    if (cont == 1):
        return("PRE " + palavra)
    else:
        return("IDE " + palavra)
