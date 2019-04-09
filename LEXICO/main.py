#Código principal do compilador
# -*- coding: utf-8 -*-
import os
import AutomatoIdentificador as identi
import AutomatoComentario as coment
#MAIN METOD
diretorio = os.getcwd()+"/teste/"
names_arq = os.listdir(diretorio)

DELIMITADORES = [' ', '/', ':', ',', '(',')', '[', ']', '{', '}']

for file in names_arq:
	print(diretorio+file)
	with open(diretorio+file) as arq:
		linhas = arq.readlines()
		palavras = []
		for linha in linhas:
			#print(linha)
			palavra = ''
			for carac in linha:
				print(carac)
				if(carac not in DELIMITADORES):
					palavra+=carac
				else:
					palavras.append(palavra)
					palavra = ''
					if carac != ' ' and carac !='\n':
						palavras.append(carac)

			print(palavras)
