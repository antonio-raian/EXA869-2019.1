# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 2019

@author: Antonio Raian e Diogo Lima
"""
import string

DELIMITADORES = ['',' ', ':', ',', ';', '(',')', '[', ']', '{', '}', '\n']
RELACIONAIS = ['=', '==', '!=', '<', '>', '<=', '>=']
ARITMETICOS = ['+', '-', '*', '/', '++', '--']
LOGICOS = ['&&', '||', '!']
SIMBOLOS = ['@','#', '$', '%', '&', '?']

def automato_delimitador(palavra):
    if(palavra in DELIMITADORES):
        return ('2',"DEL " + palavra)
    elif (palavra in RELACIONAIS):
        return ('2',"REL " + palavra)
    elif (palavra in ARITMETICOS):
        return ('2',"ARI " + palavra)
    elif (palavra in LOGICOS):
        return ('2',"LOG " + palavra)
    elif (palavra in SIMBOLOS):
        return ('2',"SIM " + palavra)
    else:
        return ('0', '')