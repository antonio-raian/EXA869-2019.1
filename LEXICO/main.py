#CÃ³digo principal do compilador
# -*- coding: utf-8 -*-
import os
import AutomatoIdentificador as aut_identi
import AutomatoComentario as aut_coment
import AutomatoNumeros as aut_numero
import AutomatoDelimitador as aut_delimitador
import AutomatoCadeia as aut_cadeia
#MAIN METOD
diretorio = os.getcwd()+"/teste/"
diretorioSaida = os.getcwd()+"/resultados/"
if(os.path.isdir(diretorioSaida)):
	print("Já tem a pasta de resultados")
else:
	os.mkdir(diretorioSaida)
names_arq = os.listdir(diretorio)

DELIMITADORES = ['',' ', ':', ',', ';', '(',')', '[', ']', '{', '}', '\n']
NUMEROS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
RELACIONAIS = ['=', '<', '>', '!'] #'==', '!=', '<=', '>='
ARITMETICOS = ['+', '-', '*', '/'] #'++', '--'
SIMBOLOS = ['@','#', '$', '%', '&', '?']  #'&&', '||'

for file in names_arq:
	numLinha = 0
	coment = 0
	print(diretorio+file)
	nomeArqAtual = os.path.basename(file)
	output = open(diretorioSaida + 'Saída_'+file, 'w')

	with open(diretorio+file) as arq:
		linhas = arq.readlines()
		linhas1 = []
		bloco = False
		linhaBloco = 0
		erros = []

		# Primeiro verifica se tem comentários e os remove
		for linha in linhas:
			numLinha+=1
			comentRes = aut_coment.automato_comentario(bloco, linha)
			if(bloco):
				if(comentRes == 2): #Encontrou comentário de bloco
					bloco = not(bloco) #Muda a variavel de auxilio pra buscar de forma diferente no automato
					linhas1.append(linha[linha.index('*/')+2:]) #Pega a depois do comentario
			else:
				if(comentRes == 0): #Deu erro na formação de comentario
					output.write(str(numLinha)+" CoMF")
					output.write('\n')
				elif(comentRes == 1): #Encontrou comentário de linha
					linhas1.append(linha[:linha.index('//')]) #Pega a linha até o comentario aparecer
				elif(comentRes == 2): #Encontrou comentário de bloco
					bloco = not(bloco) #Muda a variavel de auxilio pra buscar de forma diferente no automato
					linhaBloco = numLinha #salva a linha em que o comentário de bloco começa
				elif(comentRes == 3): #Não possui comentário na linha
					linhas1.append(linha)
		if(bloco): #Se terminar as linhas e ainda estiver num bloco, tem má formação
			erros.append(str(linhaBloco)+" CoMF \n")
		
		numLinha = 0
		cadeia = False

		#Classifica as palavras q restaram
		for linha in linhas1:
			palavras = []
			numLinha+=1
			palavra = ''
			for carac in linha:
				if(cadeia):
					palavra+=carac
					if(carac == '"' or carac == '\n'):
						cadeia = not cadeia
						palavras.append(palavra)
						palavra = ''
				else:
					if(carac in DELIMITADORES):
						if(palavra != ''): #Se não estiver vazia salva o que tem
							palavras.append(palavra)
							palavra = ''
						if(carac == ' ' and '-' in palavra and palavra[len(palavra)-1]==' '):
							palavra += carac
						if(carac != ' ' and carac != '\n' ):
							palavras.append(carac)
					elif(carac in RELACIONAIS):
						if(len(palavra)>1):
							palavras.append(palavra)
							palavra = ''
							palavra += carac
						else:
							if(len(palavra)==1):
								if(palavra in RELACIONAIS and carac == '='):
									palavra += carac
									palavras.append(palavra)
									palavra = ''
								else:
									palavras.append(palavra)
									palavra = ''
									palavra += carac
							else:
								palavra += carac
					elif(carac in ARITMETICOS):
						if(len(palavra)>1):
							palavras.append(palavra)
							palavra = ''
							palavra += carac
						else:
							if(len(palavra)==1):
								if(palavra == '+' and carac =='+'):
									palavra += carac
									palavras.append(palavra)
									palavra = ''
								elif(palavra == '-'):
									if(carac == '-'):
										palavra += carac
										palavras.append(palavra)
										palavra = ''
									elif(carac == ' ' or carac in NUMEROS):
										palavra+=carac
									else:
										palavras.append(palavra)
										palavra = ''
										palavra += carac
								else:
									palavras.append(palavra)
									palavra = ''
									palavra += carac
							else:
								palavra += carac
					elif(carac == '"'):
						if(palavra!=''):
							palavras.append(palavra)
							palavra = ''
						cadeia = not cadeia
						palavra += carac
					else:
						palavra += carac
				# if(palavra!=''):
				# 	palavras.append(palavra)

			for palavra in palavras:
				result = ''

				result_DEL = aut_delimitador.automato_delimitador(palavra)
				result_IDE = aut_identi.automato_identificador(palavra)
				print(result_IDE[0])
				result_NRO = aut_numero.automato_numeros(palavra)
				result_CAD = aut_cadeia.automato_cadeia(palavra)
				if(result_IDE[0] !='0'):
					if(result_IDE[0] == '1'):
						erros.append(str(numLinha)+" "+result_IDE[1])
					else:
						result = result_IDE[1]
				elif (result_NRO[0] !='0'):
					if(result_NRO[0] == '1'):
						erros.append(str(numLinha)+" "+result_NRO[1])
					else:
						result = result_NRO[1]
				elif (result_DEL[0] !='0'):
					if(result_DEL[0] == '1'):
						erros.append(str(numLinha)+" "+result_DEL[1])
					else:
						result = result_DEL[1]
				elif (result_CAD[0] !='0'):
					if(result_CAD[0] == '1'):
						erros.append(str(numLinha)+" "+result_CAD[1])
					else:
						result = result_CAD[1]

				if(result!=''):
					output.write(str(numLinha)+" "+result)
				output.write('\n')

		output.write('====ERROS=====')
		output.write('\n')
		
		print( erros)
		for erro in erros:
			output.write(erro)
		output.close()