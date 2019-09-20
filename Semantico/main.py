import os
from Semantico import Programa as programa

#Globais
tokenAtual = ''
#Lista Tokens
#MAIN METOD
def main():
    diretorio = os.path.abspath('.')+"/saida_lexico/" #Pega os codigos de saída do lexico
    diretorioSaida = os.path.abspath('.')+"/saida_semantico/" #Pega os codigos de saída do lexico
    names_arq = os.listdir(diretorio)
    

    erro_lexicos = []

    for file in names_arq:
        output = open(diretorioSaida + file, 'w')
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

            erros = programa.main(tokens,file)
            for erro in erros:
                output.write(erro+'\n')
            output.close()
