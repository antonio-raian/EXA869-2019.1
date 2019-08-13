#Aqui vamos começar com a aplicação para o sintático
#CÃ³digo principal do compilador sintático
# -*- coding: utf-8 -*-
import os
import Programa as programa

#Globais
tokenAtual = ''
#Lista Tokens
diretorio = os.path.abspath('..')+"/LEXICO/resultados/" #Pega os codigos de saída do lexico
# diretorio = os.getcwd()+"/codigos/"
diretorioSaida = os.getcwd()+"/resultados/"
if(os.path.isdir(diretorioSaida)):
    print("Já tem a pasta de resultados")
else:
    os.mkdir(diretorioSaida)
names_arq = os.listdir(diretorio)

erro_lexicos = []

for file in names_arq:
    tokens = []
    print(diretorio+file)
    output = open(diretorioSaida + 'Sintático_'+file, 'w')
    with open(diretorio+file) as arq:
        linhas = arq.readlines()
        lexico = False
        if(not lexico):
            for linha in linhas:#nº_linha tipo valor
                # print(linha.split(' ', 2))
                if (linha !='====ERROS=====\n'):
                    if (linha != '\n'): 
                        tokens.append(linha.split(' ', 2)) #Coloca a linha em fomato de array
                else:
                    lexico = True
                    erro_lexicos.append('Erro Lexico no arquivo: '+file)
                    break
        # print(tokens)
        programa.main(tokens)#Chama o método que trata o inicio do programa
    print(erro_lexicos)
