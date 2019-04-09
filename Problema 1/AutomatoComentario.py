# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:12:18 2019

@author: Antonio Raian e Diogo Lima
"""
LINHA = 1
BLOCO = 2
ERRO = 0

#Modulo pra dizer se é comentário de bloco ou linha
def automatoNumeros(palavra):

    tam = len(palavra)
    cont = 0
    i = 0

    if(palavra[i]=='/'):
        if(palavra[i+1]=='/'):
            return LINHA
        else if (palavra[i+1]=='*'):
            return BLOCO
    return ERRO
