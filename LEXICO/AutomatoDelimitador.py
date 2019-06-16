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
        return ("DEL " + palavra)
    elif (palavra in RELACIONAIS):
        return ("REL " + palavra)
    elif (palavra in ARITMETICOS):
        return ("ARI " + palavra)
    else:
        return '0'