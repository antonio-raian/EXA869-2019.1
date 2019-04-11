# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:12:18 2019
@author: Antonio Raian e Diogo Lima
"""

def automato_aritmeticos(palavra):

    OPERADORES = ['+', '-', '*', '/', '++', '--']
    OPERADORES_STARTS = ['+', '-', '*', '/']

    if palavra in OPERADORES:
        return "ART " + palavra

    elif palavra[0] in OPERADORES_STARTS:
        return "ERR_ART " + palavra

    else:
        return '0'

def automato_relacionais(palavra):

    OPERADORES = ['!=', '==', '<', '<=', '>', '>=', '=']
    OPERADORES_STARTS = ['!', "=", "<", ">"]

    if palavra in OPERADORES:
        return "REL " + palavra

    elif palavra[0] in OPERADORES_STARTS:
        return "ERR_REL " + palavra

    else:
        return '0'

def automato_logicos(palavra):

    OPERADORES = ['!', '&&', '||']
    OPERADORES_STARTS = ['!', "&", "|"]

    if palavra in OPERADORES:
        return "LOG " + palavra

    elif palavra[0] in OPERADORES_STARTS:
        return "ERR_LOG " + palavra

    else:
        return '0'
