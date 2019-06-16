# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 2019

@author: Antonio Raian e Diogo Lima
"""
LINHA = 1
BLOCO = 2
ERRO = 0
PASS = 3

#Modulo pra dizer se é comentário de bloco ou linha
def automato_comentario(bloco, linha):

	coment = 0

	for carac in linha:
		if(not bloco):#Não identificou comentário de bloco
			if (coment == 0):
				if (carac == '/'): 
					coment +=1
			elif (coment == 1):
				if(carac == '/'):
					return LINHA
				elif (carac == '*'):
					return BLOCO
			else:
				return ERRO
		else: #Identificou comentario de bloco
			if(coment == 0):
				if(carac == '*'):
					coment = 1
			elif(coment == 1):
				if(carac == '/'):
					return BLOCO
	return PASS
