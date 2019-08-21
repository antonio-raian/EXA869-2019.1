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
        if(i==0):
            if(carac in LETRAS):
                i+=1
            elif(carac in NUMEROS):
                return ('1', "ERR_IDE "+ palavra)
            else:
                return ('0','')    
        elif carac in LETRAS or carac in NUMEROS:
            i+=1
        else:
            return ('1',"ERR_IDE " + palavra)

    cont=0
    if palavra=="principal":
        cont=1
    elif palavra=="inteiro":
        cont=1
    elif palavra=="constantes":
        cont=1
    elif palavra=="variaveis":
        cont=1
    elif palavra=="metodo":
        cont=1
    elif palavra=="resultado":
        cont=1
    elif palavra=="programa":
        cont=1
    elif palavra=="entao":
        cont=1
    elif palavra=="se":
        cont=1
    elif palavra=="senao":
        cont=1
    elif palavra=="enquanto":
        cont=1
    elif palavra=="leia":
        cont=1
    elif palavra=="escreva":
        cont=1
    elif palavra=="vazio":
        cont=1
    elif palavra=="real":
        cont=1
    elif palavra=="boleano":
        cont=1
    elif palavra=="texto":
        cont=1
    elif palavra=="verdadeiro":
        cont=1
    elif palavra=="falso":
        cont=1
    elif palavra=="sistema":
        cont=1

    if (cont == 1):
        return('2',"PRE " + palavra)
    else:
        return('2',"IDE " + palavra)
