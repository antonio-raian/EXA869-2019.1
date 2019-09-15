import sys
import os

file = ""
tokens = ""
tabelaConstantes = []
listaMetodos = []  #0 - linha, 1 - nome, 2 - parametros(array), 3 - retorno
listaTabelaVariaveis = [] #uma lista de tabelas. Cada elemento da lista é uma tabela de um método, cujo indice é o mesmo da listaMetodos
                          #[indice do metodo][indice da variavel][0] - linha da variavel, [indice do metodo][indice da variavel][1] - tipo e [indice do metodo][indice da variavel][2] - nome.
erros = [] #lista de erros semanticos para serem impressos no final da execucao
nroErro = 0
indicePrincipal = -1 #variável que diz qual é o índice do MAIN na variável listaTabelaVariaveis

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

    separaConstantes(tokens) #Remove o bloco de constantes dos Lexemas pra analise
    listarMetodos(tokens)
    listarVariaveis()
    verificarListaVariaveis()

    print(erros)


def verificarListaVariaveis(lista_tokens):
    global tabelaMetodos
    global listaTabelaVariaveis
    global indicePrincipal

    myTokens = listaTabelaVariaveis
    cont = 0


    for metodoAtual in myTokens:
        for variavel in metodoAtual:
            verificarListaVariaveisAux(cont, metodoAtual)
            cont = cont + 1
        cont = 0

def verificarListaVariaveisAux(indiceAtual, metodoAtual):
    global indicePrincipal

    variavelAtual = metodoAtual[indiceAtual]
    cont = 0
    #donothing = 0
    #estaNoPrincipal = 0

    #for variavel in metodoPrincipal:
       #if (indiceMetodoAtual == indicePrincipal):
        #    donothing = 1
        #elif(donothing == 0 and (variavel[2] == variavelAtual[2])): #mesmo nome
         #   estaNoPrincipal = 1 #sim

    for variavel in metodoAtual:

        if(cont > indiceAtual): #conta até passar dele mesmo na lista
            if(variavel[2] == variavelAtual[2]): #mesmo nome
                imprimeErroVariavel(variavelAtual[0], variavel[0], variavel[2])
        else:
            cont = cont + 1

def imprimeErroVariavel(linhaerro1, linhaerro2, nomeVariavel):
    global erros
    global nroErro

    erros.append("Erro encontrado na linha "+linhaerro2+". Nome de variável "+nomeVariavel+" idêntico, no mesmo escopo, ao encontrado na linha "+linhaerro1+".")


def listarVariaveis(lista_tokens):
    global tabelaMetodos
    global listaTabelaVariaveis
    global indicePrincipal

    myTokens = lista_tokens
    elementos = ""
    cont = 0
    x = 0
    achouMetodo = 0
    achouTipo = 0
    tipoAtual = ""
    numVariaveis = 0

    for token in myTokens:
        linha = token[0]
        tipo = token[1]
        valor = token[2]

        if(valor == 'metodo\n'):
            elementos[x] = cont
            x = x + 1

        cont = cont + 1

    cont = 0
    x = 0

    myTokens = lista_tokens
    for token in myTokens:
        linha = token[0]
        tipo = token[1]
        valor = token[2]

        if((cont == elementos[x] and achouMetodo == 0) or valor == 'principal\n'): #achou um metodo ou o main
            achouMetodo = 1
            if (valor == 'principal\n'):
                indicePrincipal = x
        elif(achouMetodo == 1 and valor == 'variaveis\n'): #achou bloco de variaveis
            achouMetodo = 2
        elif(achouMetodo == 2): #{
            achouMetodo = 3
        elif(achouMetodo == 3 and achouTipo == 0): #tipo novo ou }
            if (valor == '}\n'):
                x = x + 1 #proximo metodo a ser analisado
                tipoAtual = ""
                achouMetodo = 0
                numVariaveis = 0
            else:
                tipoAtual = valor[:-1]
                achouTipo = 1
        elif(achouMetodo == 3 and achouTipo == 1): #nome da variavel
            tabelaMetodos[x][numVariaveis][0] = linha
            tabelaMetodos[x][numVariaveis][1] = tipoAtual
            tabelaMetodos[x][numVariaveis][2] = valor[:-1]
            achouTipo = 2
            numVariaveis = numVariaveis + 1
        elif(achouMetodo == 3 and achouTipo == 2): #, ou ;
            if (valor == ',\n'):
                achouTipo == 1
            else:
                achouTipo == 0

            #x = x + 1
        cont = cont + 1

def imprimeErroMetodo(linhaerro1, linhaerro2, nomeMetodo):
    global erros
    global nroErro

    erros.append("Erro encontrado na linha "+linhaerro2+". Método "+nomeMetodo+" idêntico ao encontrado na linha "+linhaerro1+".")

def listarMetodos(lista_tokens):
    global listaMetodos

    parametros = []    
    itemTabela = []
    contParametros = 0
    myTokens = lista_tokens.copy()
    achouMetodo = 0
    cont = 0
    parenteses = 0
    retorno = 0

    while len(myTokens) > 0:
        token = myTokens.pop(0)
        linha = token[0]
        tipo = token[1]
        valor = token[2]

        if(tipo == 'PRE' and valor == 'metodo\n'):
            achouMetodo = 1
        elif(achouMetodo == 1): #nome do metodo
            achouMetodo = 2
            itemTabela.append(linha)
            itemTabela.append(valor[:-1]) #Nome do metodo

            # listaMetodos[cont][0] = linha
            # listaMetodos[cont][1] = valor[:-1]
        elif(achouMetodo == 2 and valor == '(\n'): #(
            itemParam = []
            while token[2]!=')\n':
                token = myTokens.pop(0)
                linha = token[0]
                tipo = token[1]
                valor = token[2]

                if(valor !=')\n'):
                    if(valor !=',\n'):                    
                        itemParam.append(valor)
                    else:
                        parametros.append(itemParam)
                        itemParam = []
                else:
                    parametros.append(itemParam)
            retorno = 1
            itemTabela.append(parametros)
        elif(retorno == 1 and tipo == 'PRE'):
            itemTabela.append(valor)
            if(verificaMetodo(itemTabela)):
                listaMetodos.append(itemTabela)
                itemTabela = []
            retorno = 0
            achouMetodo = 0

def verificaMetodo(item):
    global listaMetodos

    for metodo in listaMetodos:
        iguais = 0
        if(item[1] == metodo[1]): #nome igual
            paramsItem = item[2]
            paramsMetodo = metodo[2]
            if(len(paramsItem) == len(paramsMetodo)):# Se a quantidade de parametros for a mesma Há a possibilidade de serem iguais
                i = 0
                for param in paramsMetodo: #Percorre os parametros
                    if(param[0] == paramsItem[i][0]): #Vai contando a quantidade de parametros iguais
                        iguais = iguais + 1
                    else: #Se algum for diferente para
                        break
                    i += 1
                if(iguais == len(paramsItem)): #Se todos os param forem iguais tá errado
                    imprimeErroMetodo(metodo[0], item[0], item[1] )
                    return False
    return True

def separaConstantes(lista_tokens):
    global tokens
    myTokens = lista_tokens
    cont = 0
    achouConstantes = 0

    for token in lista_tokens:
        linha = token[0]
        tipo = token[1]
        valor = token[2]

        if(achouConstantes == 1): #Já encontrou o bloco constantes... agora procura a proxima }
            if(valor == '}\n'):
                tokens = myTokens[cont-1:]
                myTokens = myTokens[:cont-1] #Corta o vetor de forma que possua apenas de CONSTANTES até }
                achouConstantes = 0
                break

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
        itemTabela = []
        linha = token[0]
        tipo = token[1]
        valor = token[2]

        if(tipo == 'PRE' and valor != 'constantes\n'): #Achou nova tipagem de constante
            tipagemAtual = valor
        elif(tipo == 'IDE'): #Achou novo nome de constante
            itemTabela.append(linha)
            itemTabela.append(tipagemAtual) #Referente à tipagem da constante. Não confundir com 'tipo', que é o tipo do TOKEN, não da variável
            itemTabela.append(valor)

            tabelaConstantes.append(itemTabela)
            
            #Não é necessário salvar o contexto, pois essa tabela é própria para constantes
            ultimaConstante = valor
        elif(valor != '=\n' and valor != ',\n' and valor != '{\n' and valor != '}\n' and valor != ';\n' and valor != 'constantes\n'):#Eliminadas todas a possibilidades, resta apenas o VALOR ATRIBUIDO
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

    erros.append("Erro encontrado na linha "+linhaerro+". Atribuição inadequada para constante <"+ultimaConstante+">, que possui o tipo "+tipagemErro+".")