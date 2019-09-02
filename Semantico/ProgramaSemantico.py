import sys
import os

file = ""
tokens = ""
tabelaConstantes = ""
listaMetodos = ""
tabelaMetodos = "" #uma lista de tabelas. Cada elemento da lista é uma tabela de um método, cujo indice é o mesmo da listaMetodos
erros = "" #lista de erros semanticos para serem impressos no final da execucao
nroErro = 0

def main(lista_tokens, arq):
	global tokens
	global file
	global output

	tokens = lista_tokens
	file = arq
	diretorioSaida = os.path.abspath('.')+"/saida_semantico/"
	if(not os.path.isdir(diretorioSaida)):
		os.mkdir(diretorioSaida)
	
	output = open(diretorioSaida +file, 'w')

	separaConstantes(lista_tokens)

def separaConstantes(lista_tokens):
	myTokens = lista_tokens
	cont = 0
	achouConstantes = 0

	for token in lista_tokens:
		linha = token[0]
		tipo = token[1]
		valor = token[2]

		if(achouConstantes == 1): #Já encontrou o bloco constantes... agora procura a proxima }
			if(valor == '}\n'):
				myTokens = myTokens[:cont] #Corta o vetor de forma que possua apenas de CONSTANTES até }
				achouConstantes = 0

		elif(valor == 'constantes\n'): #Procura o bloco constantes
			myTokens = myTokens[cont:] #Corta o vetor de forma que possua apenas de CONSTANTES em diante
			achouConstantes = 1
		
		cont = cont + 1

	mapeiaConstantes(myTokens)


def mapeiaConstantes(lista_tokens):
	global tabelaConstantes

	i = 0
	tipagemAtual = ""
	ultimaConstante = ""

	for token in lista_tokens:
		linha = token[0]
		tipo = token[1]
		valor = token[2]

		if(tipo == 'PRE' and valor != 'constantes\n'): #Achou nova tipagem de constante
			tipagemAtual = valor
		elif(tipo == 'IDE') #Achou novo nome de constante
			tabelaConstantes[i][0] = linha
			tabelaConstantes[i][1] = tipagemAtual #Referente à tipagem da constante. Não confundir com 'tipo', que é o tipo do TOKEN, não da variável
			tabelaConstantes[i][2] = valor
			i = i + 1
			#Não é necessário salvar o contexto, pois essa tabela é própria para constantes
			ultimaConstante = valor
		elif(valor == '=\n' or valor == ',\n' or valor == '{\n' or valor == '}\n' or valor == 'constantes\n'):
			i = i #do nothing
		else: #Eliminadas todas a possibilidades, resta apenas o VALOR ATRIBUIDO
			if (tipagemAtual == 'boleano\n'):
				if (valor != 'verdadeiro\n' and valor != 'falso\n'): #atribuicao errada
					imprimeErroConstante(str(linha), ultimaConstante[:-1], tipagemAtual[-1])

			elif(tipagemAtual == 'texto\n'):
				if (tipo != 'CAD'): #atribuicao errada
					imprimeErroConstante(str(linha), ultimaConstante[:-1], tipagemAtual[-1])

			elif(tipagemAtual == 'inteiro\n'):
				if (tipo != 'NRO' or "." in valor): #atribuicao errada OU é um real
					imprimeErroConstante(str(linha), ultimaConstante[:-1], tipagemAtual[-1])

			elif(tipagemAtual == 'real\n'):
				if not(tipo == 'NRO' and "." in valor): #atribuicao errada OU é um inteiro
					imprimeErroConstante(str(linha), ultimaConstante[:-1], tipagemAtual[-1])


def imprimeErroConstante(linhaerro, ultimaConstante, tipagemErro):
	global erros
	global nroErro

	erros[nroErro] = "Erro encontrado na linha "+linhaerro+". Atribuição inadequada para constante <"+ultimaConstante+">, que possui o tipo "+tipagemErro+"."
	nroErro = nroErro + 1




