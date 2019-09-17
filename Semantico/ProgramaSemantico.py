import sys
import os

file = ""
tokens = ""
tabelaConstantes = []
listaMetodos = []  #0 - linha, 1 - nome, 2 - parametros(array), 3 - retorno
listaTabelaVariaveis = [] #uma lista de tabelas. Cada elemento da lista é uma tabela de um método, cujo indice é o mesmo da listaMetodos
                          #[indice do metodo][indice da variavel][0] listaTabela- linha da variavel, [indice do metodo][indice da variavel][1] - tipo e [indice do metodo][indice da variavel][2] - nome.
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
    listarMetodos(tokens) #Coloca os metodos numa lista e verifica a igualdade entre os mesmos
    listarVariaveis(tokens)
    verificarListaVariaveis(tokens)
    verificaExistenciaVariavel(tokens)
    verificaAtribuicaoVariavel(tokens)

    print(erros)

    for erro in erros:
        output.write(erro)
    output.close

def verificaExistenciaVariavel(lista_tokens):
    global tabelaMetodos
    global listaTabelaVariaveis
    global indicePrincipal

    myTokens = lista_tokens
    indiceMetodoAtual = -1
    varcontrole = 0
    cont = 0
    varExiste = 0
    ideAtual = ""


    for token in lista_tokens:
        linha = token[0]
        tipo = token[1]
        valor = token[2]

        if(valor == 'metodo\n'):
            indiceMetodoAtual = indiceMetodoAtual + 1 #pega a referencia do metodo atual

        if(tipo == 'IDE'): #achou um IDE
            
            for metodo in listaTabelaVariaveis:
                if (cont == indiceMetodoAtual or cont == indicePrincipal):
                    for variavel in metodo:
                        print(metodo)
                        print(variavel)
                        if (variavel[0][2] == ideAtual): #se o nome da variavel for o mesmo nome...
                            varExiste = 1
                    cont = cont + 1
                    if(varExiste == 1):
                        varExiste == 0
                    else:
                        imprimeErroExistenciaVariavel(listaMetodos[indiceMetodoAtual][1], valor[:-1])

def imprimeErroExistenciaVariavel(nomeMetodo, nomeVariavel):
    global erros
    global nroErro

    erros.append("Variavel/constante de nome "+nomeVariavel+" usada no metodo "+nomeMetodo+" nao foi inicializada.")

def imprimeErroAtribuicaoConstante(linha, nomeVariavel):
    global erros
    global nroErro

    erros.append("Constante de nome "+nomeVariavel+" recebendo atribuicao na linha "+linha)

def imprimeErroAtribuicaoVariavel(linha, nomeVariavel):
    global erros
    global nroErro


    print(nomeVariavel)
    print(linha)
    erros.append("Atribucao na linha "+linha[0]+" de um tipo incorreto da variavel "+nomeVariavel)


def verificaAtribuicaoVariavel(lista_tokens):
    global tabelaMetodos
    global listaTabelaVariaveis
    global indicePrincipal

    myTokens = lista_tokens
    indiceMetodoAtual = -1
    varcontrole = 0
    cont = 0
    varExiste = 0
    ideAtual = ""
    tipoAtual = ""
    tipoComparar = ""


    for token in lista_tokens:
        linha = token[0]
        tipo = token[1]
        valor = token[2]

        if(valor == 'metodo\n'):
            indiceMetodoAtual = indiceMetodoAtual + 1 #pega a referencia do metodo atual

        if(tipo == 'IDE' and varcontrole == 0): #achou um IDE
            varcontrole = 1
            ideAtual = valor[:-1]
            for metodo in listaTabelaVariaveis:
                if (cont == indiceMetodoAtual):
                    for variavel in metodo:
                        if (variavel[0][2] == valor[-1]): #se o nome da variavel for o mesmo nome...
                            tipoAtual = variavel[1]
                elif(cont == indicePrincipal):
                    for variavel in metodo:
                        if (variavel[2] == valor[-1]): #se o nome da variavel for o mesmo nome...
                            imprimeErroAtribuicaoConstante(variavel[0], variavel[2])
            cont = 0
        elif(valor == '=\n' and varcontrole == 1): #todo IDE sucedido de = sem outro = na frente é atribuição
            varcontrole = 2
        elif(valor == '(\n' and varcontrole == 2): #pode achar ( ou IDE ou NRO... ou PRE
            #not treated...

            cont = 0
            varcontrole = 0
        elif(tipo == 'NRO' and varcontrole == 2):
            if(tipoAtual != 'real' and tipoAtual != 'inteiro'):
                imprimeErroAtribuicaoVariavel(variavel[0], ideAtual)
            elif(tipoAtual == 'real' and '.' not in valor):
                imprimeErroAtribuicaoVariavel(variavel[0], ideAtual)
            elif(tipoAtual == 'inteiro' and '.' in valor):
                imprimeErroAtribuicaoVariavel(variavel[0], ideAtual)

            cont = 0
            varcontrole = 0

        elif(valor == 'IDE' and varcontrole == 2):
            for metodo in listaTabelaVariaveis:
                if (cont == indiceMetodoAtual or cont == indicePrincipal):
                    for variavel in metodo:
                        if (variavel[2] == valor[-1]): #se o nome da variavel for o mesmo nome...
                            tipoComparar = variavel[1]

                            if (tipoComparar != tipoAtual): #se o tipo da variavel enontrada for diferente do tipo da variavel sendo atribuida
                                imprimeErroAtribuicaoVariavel(variavel[0], ideAtual)
                    cont = cont + 1

            cont = 0
            varcontrole = 0
        elif(valor == 'PRE' and varcontrole == 2):
            if(valor[:-1] != 'verdadeiro' and valor[:-1] != 'falso'):
                imprimeErroAtribuicaoVariavel(variavel[0], ideAtual)
            elif(tipoAtual != 'boleano'):
                imprimeErroAtribuicaoVariavel(variavel[0], ideAtual)
   
            cont = 0
            varcontrole = 0

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
    elementos = []
    cont = 0
    x = 0
    achouMetodo = 0
    achouTipo = 0
    tipoAtual = ""
    numVariaveis = 0
    auxnum = []
    auxnum3 = []



    for token in myTokens:
        linha = token[0]
        tipo = token[1]
        valor = token[2]

        if(valor == 'metodo\n'):
            elementos.append(cont)
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
            auxnum2 = []
            auxnum2.append(linha)
            auxnum2.append(tipoAtual)
            auxnum2.append(valor[:-1])
            auxnum.append(auxnum2)
        
            auxnum3.append(auxnum)
            #listaTabelaVariaveis[x].append(auxnum)
            auxnum = []
            achouTipo = 2
            numVariaveis = numVariaveis + 1
        elif(achouMetodo == 3 and achouTipo == 2): #, ou ;
            if (valor == ',\n'):
                achouTipo == 1
            else:
                listaTabelaVariaveis.append(auxnum3)
                
                auxnum3 = []
                achouTipo == 0

            #x = x + 1
        cont = cont + 1


def imprimeErroMetodo(linhaerro1, linhaerro2, nomeMetodo):
    global erros
    global nroErro

    erros.append("Erro encontrado na linha "+linhaerro2+". Método "+nomeMetodo+" idêntico ao encontrado na linha "+linhaerro1+".")

def erroRetornoMetodo(linha, metodo):
    global erros
    erros.append("Erro encontrado na linha "+linha+". Método "+metodo[1]+" esperado resultado "+metodo[3]+" .")

def listarMetodos(lista_tokens):
    global listaMetodos

    parametros = []    
    itemTabela = []
    metodoAtual = []
    myTokens = lista_tokens.copy()
    achouMetodo = 0
    retorno = 0

    while len(myTokens) > 0:
        token = myTokens.pop(0)
        linha = token[0]
        tipo = token[1]
        valor = token[2]

        if(tipo == 'PRE'):
            if(valor == 'metodo\n'):
                achouMetodo = 1
            elif(retorno == 1):
                itemTabela.append(valor)
                if(verificaMetodo(itemTabela)):
                    listaMetodos.append(itemTabela)
                    metodoAtual = itemTabela.copy()
                    itemTabela = []
                retorno = 0
                achouMetodo = 0
            elif(valor == 'resultado\n'):
                token = myTokens.pop(0)
                linha = token[0]
                tipo = token[1]
                valor = token[2]
                if(tipo == 'PRE'):
                    if(valor == 'vazio\n' and metodoAtual[3] != 'vazio\n'):
                        erroRetornoMetodo(linha, metodoAtual)
                #elif(tipo == 'IDE'):
                    #var = pegaVariavel(valor, metodoAtual)
                    #const = verificaConstante(token)
                    #if(var):
                        #if(metodoAtual[3] != var[2]):
                            #erroRetornoMetodo(linha, metodoAtual)
                    #elif(const):
                        #if(metodoAtual[3] != const[2]):
                            #erroRetornoMetodo(linha, metodoAtual)
                #else:
                    #erroRetornoMetodo(linha, metodoAtual)
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

        if(tipo == 'PRE' and valor != 'constantes\n' and valor != 'falso\n' and valor != 'verdadeiro\n'): #Achou nova tipagem de constante
            tipagemAtual = valor
        elif(tipo == 'IDE'): #Achou novo nome de constante
            itemTabela.append(linha)
            itemTabela.append(tipagemAtual) #Referente à tipagem da constante. Não confundir com 'tipo', que é o tipo do TOKEN, não da variável
            itemTabela.append(valor)

            if(verificaConstante(itemTabela) == True):
                tabelaConstantes.append(itemTabela)
            else:
                imprimeErroConstante(linha, ultimaConstante, tipagemAtual)
            
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

def verificaConstante(item):
    global tabelaConstantes

    for constante in tabelaConstantes:
        if(constante[2] == item[2]):
            return constante
    return True

def imprimeErroConstante(linhaerro, ultimaConstante, tipagemErro):
    global erros
    global nroErro

    erros.append("Erro encontrado na linha "+linhaerro+". Atribuição inadequada para constante <"+ultimaConstante+">, que possui o tipo "+tipagemErro+".")

def pegaVariavel(nome, escopo):
    global listaTabelaVariaveis
    global listaMetodos

    indice = listaMetodos.index(escopo)
    print(listaTabelaVariaveis)
    variaveisMetodo = listaTabelaVariaveis[indice]

    for variavel in variaveisMetodo:
        if(variavel[2] == nome):
            return variavel
    return False
