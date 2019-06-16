# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:12:18 2019

@author: Antonio Raian e Diogo Lima
"""

def automato_numeros(palavra):

    tamanho = len(palavra)
    i = 0
    fim = 0
    print ('NUMERO')
    print (palavra)
    if palavra[i] == '-': #Verifica se tem um menos no começo da funcao
        i = i+1
        while fim < 1: #Ignora os espaços entre o - e o numero
            if palavra[i] == ' ':
                i = i+1
            else: 
                fim = 1
    fim = 0

    if palavra[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        while fim < 1:
            if palavra[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                i = i+1

                if i == tamanho: # Fim da palavra, sucesso (não possui casas decimais) """
                    return "NRO " + palavra
            else:
                fim = 1

        fim = 0

        if palavra[i] == '.':
            i = i+1
            if i == tamanho: #"""Fim da palavra, ERRO DE NUMERO"""
                return "ERR_NRO " + palavra


            if palavra[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):

                while fim < 1:
                    if palavra[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        i = i+1

                        if i == tamanho:
                            return "NRO " + palavra #""" Fim da palavra, sucesso (possui casas decimais) """
                    else:
                        return "ERR_NRO " + palavra #""" Erro, caractere diferente de número após a primeira casa decimal """
            else:
                return "ERRO DE IMPLEMENTAÇÃO DO SCANNER (Passou lexema sem usar . como delimitador" + palavra #""" Erro, caractere diferente de número após o ponto """
        else:
            return "ERR_NRO " + palavra #""" Erro, algo diferente de um ponto depois do último número inteiro """
    else:
        return '0' #""" Erro, autômato não consumiu nada """
