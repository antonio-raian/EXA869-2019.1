#Aqui vamos começar com a aplicação para o sintático
#CÃ³digo principal do compilador sintático
# -*- coding: utf-8 -*-
import os
from SINTATICO import Programa as programa

#Globais
tokenAtual = ''
#Lista Tokens
#MAIN METOD
def main():
    diretorio = os.path.abspath('.')+"/saida_lexico/" #Pega os codigos de saída do lexico
    names_arq = os.listdir(diretorio)

    erro_lexicos = []

    for file in names_arq:
        tokens = []
        print(diretorio+file)
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
            if(programa.main(tokens, file)):#Chama o método que trata o inicio do programa
                print('Deu bom')
            else:
                print('Deu ruim')
        
        print(erro_lexicos)
