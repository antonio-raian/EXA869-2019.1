#CÃ³digo principal do compilador
# -*- coding: utf-8 -*-
import os
import AutomatoIdentificador as aut_identi
import AutomatoComentario as aut_coment
import AutomatoNumeros as aut_numero
#MAIN METOD
diretorio = os.getcwd()+"/teste/"
names_arq = os.listdir(diretorio)

DELIMITADORES = [' ', '/', ':', ',', '(',')', '[', ']', '{', '}', '\n']

for file in names_arq:
	numLinha = 0
	print(diretorio+file)
	nomeArqAtual = os.path.basename(file)
	output = open(nomeArqAtual, 'w')

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

			for palavra in palavras:
				result = ''

				result_IDE = aut_identi.automato_identificador(palavra)
				result_NRO = aut_numero.automato_numeros(palavra)
				#result_CMT = aut_coment.automato_comentario(palavra)
				if(result_IDE !='0'):
					result = result_IDE
				elif (result_NRO !='0'):
					result = result_NRO
				#else:
					#result = "Err "+palavra
				print(str(numLinha)+" "+result)
				output.write(str(numLinha)+" "+result)
				output.write('\n')
			print(palavras)
		output.close()