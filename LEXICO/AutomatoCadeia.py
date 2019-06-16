# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:12:18 2019
@author: Antonio Raian e Diogo Lima
"""
import string

LETRAS = list(string.ascii_letters)
NUMEROS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SIMBOLOS = [' ', '!', '#', '$', '%', '&', '(', ')', '*', '+', '-', ',', '.', '/', ':', ';', '<', '>', '=', '?', '@', '[', ']', '^', '_', '`', '{', '}', '|', '~', '\'', '\\', '"']

#Deve-se passar como argumento tudo a partir da primeira aspas, e o proprio automato faz a separacao.
#O return desse automato é sempre um vetor de 2 posicoes. Leia os comentários para entender melhor

def automato_cadeia(palavra):

    aspas = False

    if(palavra[0]!='"'):
        return ('0', '')
    else:
        if(palavra[len(palavra)-1] != '"'):
            return ('1','CaMF '+palavra)

    for carac in palavra:
        if(carac not in LETRAS and carac not in NUMEROS and carac not in SIMBOLOS):
            return ('2','Err_CAD '+palavra)
    
    return ('2','CAD '+ palavra)