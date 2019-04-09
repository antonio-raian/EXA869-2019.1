# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 2019

@author: Antonio Raian e Diogo Lima
"""
import string
LETRAS = list(string.ascii_leters)
NUMEROS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']

def automato_identificador(palavra):
    i = 0
    for carac in palavra:
        if(carac in LETRAS || carac in numeros):
            i++
        else:
            return i

    return i
