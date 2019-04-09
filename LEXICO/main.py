#Código principal do compilador
# -*- coding: utf-8 -*-
import os
import AutomatoIdentificador as identi
import AutomatoComentario as coment
#MAIN METOD
diretorio = os.getcwd()+"/teste/"
names_arq = os.listdir(diretorio)

DELIMITADORES = [' ', '/', ':', ',', '(',')', '[', ']', '{', '}', '\n']

for file in names_arq:
	numLinha = 0
	print(diretorio+file)
	with open(diretorio+file) as arq:
		linhas = arq.readlines()

		for linha in linhas:
			palavras = []
			numLinha+=1
			palavra = ''
			for carac in linha:
				if(carac not in DELIMITADORES):
					palavra+=carac
				else:
					if(palavra!=''):
						palavras.append(palavra)
						palavra = ''
					if carac != ' ' and carac !='\n':
						palavras.append(carac)
			if(palavra!=''):
				palavras.append(palavra)
			print(palavras)
