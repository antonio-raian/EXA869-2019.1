# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:12:18 2019
@author: Antonio Raian e Diogo Lima
"""
import string

#Deve-se passar como argumento tudo a partir da primeira aspas, e o proprio automato faz a separacao.
#O return desse automato é sempre um vetor de 2 posicoes. Leia os comentários para entender melhor

def automato_cadeia(palavra):

    LETRAS = list(string.ascii_letters)
    NUMEROS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    SIMBOLOS = [' ', '!', '#', '$', '%', '&', '(', ')', '*', '+', '-', ',', '.', '/', ':', ';', '<', '>', '=', '?', '@', '[', ']', '^', '_', '`', '{', '}', '|', '~', '\'', '\\']

    tamanho = len(palavra)

    last_carac = ''
    added_caracs = ''
    end = 0
    i = 0
    invalido = 0

    for carac in palavra:
        if i == 0 and carac != '"': #O primeiro caractere deve ser uma aspa, caso contrario, nao consome nada
            return ['0', '0']

        if carac in LETRAS or carac in NUMEROS or carac in SIMBOLOS:
            last_carac = carac
            i = i + 1

        elif carac == '"':
            added_caracs = last_carac + carac
            i = i + 1

            if added_caracs != '\\"': #Verifica se a aspas é prececida de backslash. Se for, trata como um caractere mundano
                if end == 0: #Protocolo para ignorar a primeira aspas
                    end = end + 1
                else:
                    if invalido == 0: #verifica se a CDC teve algum caractere invalido
                        return ["CDC "+palavra[:i], palavra[i:]]   #Retorna um vetor, cuja primeira parte é o token + o lexema, e a segunda parte é o restante da palavra apos a cadeia
                    else:
                        return ["ERR_CDC "+palavra[:i], palavra[i:]] #Retorna um vetor, cuja primiera parte é o token de erro + o lexema, ^^^^^^^^

            else:
                last_carac = carac

        else: #caractere invalido, deve-se ler a string até o final e então demarcar o erro
            invalido = invalido + 1

    return ["ERR_CDC "+palavra, ''] #chegando aqui, todo o texto do arquivo foi consumido antes que se pudesse achar um fim para a cadeia de caracteres
