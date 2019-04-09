# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 2019

@author: Antonio Raian e Diogo Lima
"""

def automatoNumeros(palavra):

    tamanho = len(palavra)
    i = 0
    fim = 0

    if palavra[i] == '-':

        i = i+1
        while fim < 1:
            if palavra[i] == ' ':
                i = i+1
            else:
                fim = 1

    fim = 0

    if palavra[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        i = i+1

        while fim < 1:
            if palavra[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                i = i+1

                if i == tamanho: """ Fim da palavra, sucesso (não possui casas decimais) """
                    return 1
            else
                fim = 1

        fim = 0

        if palavra[i] == '.':
            i = i+1

            if palavra[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                i = i+1

                while fim < 1:
                    if palavra[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        i = i+1

                        if i == tamanho:
                            return 1 """ Fim da palavra, sucesso (possui casas decimais) """
                    else:
                        return 0 """ Erro, caractere diferente de número após a primeira casa decimal """
            else:
                return 0 """ Erro, caractere diferente de número após o ponto """
        else:
            return 0 """ Erro, algo diferente de um ponto depois do último número inteiro """
    else:
        return 0 """ Erro, palavra inicia com algo diferente de '-' ou número """
