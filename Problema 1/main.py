#Código principal do compilador
# -*- coding: utf-8 -*-
import os
#MAIN METOD
diretorio = os.getcwd()+"/teste/"
names_arq = os.listdir(diretorio)

for file in names_arq:
	carac= []
	print(diretorio+file)
	with open(diretorio+file) as arq:
		linhas = arq.readlines()
		for linha in linhas:
			for caractere in linha:
				carac.append(caractere)
	print(carac)