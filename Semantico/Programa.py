import sys
import os

file = ""
tokens = ""
tabelaConstantes = []
listaMetodos = []  #0 - linha, 1 - nome, 2 - parametros(array), 3 - retorno

erros = [] #lista de erros semanticos para serem impressos no final da execucao
nroErro = 0

def main(lista_tokens, arq):
    global tokens
    global file
    global output

    tokens = lista_tokens.copy()
    file = arq
    diretorioSaida = os.path.abspath('.')+"/saida_semantico/"
    if(not os.path.isdir(diretorioSaida)):
        os.mkdir(diretorioSaida)
    
    output = open(diretorioSaida +file, 'w')

    analisaConstantes(tokens)
    #Nesse ponto os tokens não possuem mais as constantes e a tabela de constantes está preenchida
    analisaMetodos(tokens)
    return True
#Constantes ------------------------------- 
def analisaConstantes(tokens):
    global tabelaConstantes

    fim_bloco = False
    while not fim_bloco:
        token = ''
        token = tokens.pop(0)
        if(token[2]=='constantes\n'):
            bloco_const = separaBloco(tokens)
            mapeiaDeclaracao(tabelaConstantes, bloco_const)
            if(len(bloco_const)<=0):
                fim_bloco = True

def imprimeErroConstante(tipo, item):
    global erros

    if(tipo == 0): #Constante com nome já declarado
        erros.append("Erro encontrado na linha "+item[0]+". Já existe constante "+item[2]+".")
    elif(tipo == 1): #Erro de tipagem, tentando armazenar um valor que não é do mesmo tipo da constante
        erros.append("Erro encontrado na linha "+item[0]+". Atribuição inadequada para constante para o tipo "+item[1]+".")
#-----------------------------------------------------------------------------
#Variaveis -----------------------------
def imprimeErroVariavel(tipo, item):
    global erros

    if(tipo == 0): #Variavel com nome já declarado
        erros.append("Erro encontrado na linha "+item[0]+". Já existe veriavel "+item[2]+".")
    elif(tipo == 1): #Erro de tipagem, tentando armazenar um valor que não é do mesmo tipo da Variavel
        erros.append("Erro encontrado na linha "+item[0]+". Atribuição inadequada para variavel para o tipo "+item[1]+".")
    elif(tipo == 2):# Erro de variavel não declarada
        erros.append("Erro encontrado na linha "+item[0]+". Variavel não encontrada "+item[2]+".")
    elif(tipo == 3):#Erro de tipo de variavel
        erros.append("Erro encontrado na linha "+item[0]+". Variavel "+item[2]+" precisa ser do tipo "+item[1]+".")
#-----------------------------------------------------------------------------
#Metodos -------------------------------
def analisaMetodos(tokens):
    global listaMetodos
    global erros

    fim_programa = False
    num_metodo = -1
    while not fim_programa:
        num_metodo = num_metodo + 1
        token = ''
        token = tokens.pop(0)
        if(token[2]=='metodo\n'):
            tabela_variaveis = []
            mapeiaMetodo(tokens)
            #Nesse ponto aq os tokens não possuem mais a declaração do metodo e o topo é {
            bloco_metodo = separaBloco(tokens)
            #Nesse ponto os tokens não possuem mais o metodo em analise, o metodo está em bloco metodo
            while len(bloco_metodo)>0:
                token = bloco_metodo.pop(0)
                [linha, tipo, valor] = token
                if(valor == 'variaveis\n'):
                    bloco_variaveis = separaBloco(bloco_metodo) 
                    mapeiaDeclaracao(tabela_variaveis, bloco_variaveis) #No fim a tabela de variaveis deve estar preenchida
                elif(tipo == 'PRE'):
                    if(valor == 'leia\n'):
                        inst_leia = []
                        while valor != ';\n':
                            token = bloco_metodo.pop(0)
                            [linha, tipo, valor] = token                            
                            inst_leia.append(token) #Ao fim o inst_leia será a instrução sem o 'leia'
                        analisaLeia(inst_leia, tabela_variaveis)
                    elif(valor == 'escreva\n'):
                        inst_escreva = []
                        while valor != ';\n':
                            token = bloco_metodo.pop(0)
                            [linha, tipo, valor] = token                            
                            inst_escreva.append(token) #Ao fim o inst_escreva será a instrução sem o 'escreva'
                        analisaEscreva(inst_escreva, tabela_variaveis)
                    elif(valor == 'se\n'):
                        pass
                        # analisaLogicaSe(bloco_metodo)
                        #Nesse ponto bloco_metodo não terá mais a declaração do se
                    elif(valor == 'enquanto\n'):
                        pass
                    elif(valor == 'resultado\n'):
                        analisaResultado(bloco_metodo, listaMetodos[num_metodo][3], tabela_variaveis)
                elif(tipo == 'IDE'):
                    pass

        elif(token[2] == 'principal\n'):
            True

def mapeiaMetodo(tokens):
    global listaMetodos

    fim_declaracao = False
    in_parametros = False
    parametros = []
    item_parametro = []
    while not fim_declaracao:
        item_tabela = []
        token = tokens.pop(0)
        [linha, tipo, valor] = token
        if(in_parametros):
            if(tipo == 'PRE'):
                item_parametro.append(valor)
            elif(tipo == 'IDE'):
                item_parametro.append(valor)
                parametros.append(item_parametro)
                item_parametro = []
            elif (valor == ')\n'):
                in_parametros = False
        elif(tipo == 'IDE'):
            item_tabela.append(linha)
            item_tabela.append(valor)
        elif(valor == '(\n'):
            in_parametros = True
        elif(tipo == 'PRE'):
            item_tabela.append(valor)
            if(validaMetodo(item_tabela)):
                listaMetodos.append(item_tabela)
            else:
                imprimeErroMetodo(item_tabela)
            fim_declaracao = True

def validaMetodo(item):
    global listaMetodos

    for metodo in listaMetodos: #Para cada metodo em Lista metodo
        if(metodo[1] == item[1]): #Verifica se o nome é igual, se for igual
            if(len(metodo[2]) == len(item[2])): #Verifica se a quantidade de parametros é a mesma, se for
                qtd_igual = 0
                for paramMetodo in metodo[2]: #Para cada parametro do metodo da lista
                    for paramItem in item[2]: #Para cada parametro do metodo em analise
                        if(paramMetodo[0] == paramItem[0]): #Se algum parametro tiver o mesmo tipo
                            qtd_igual = qtd_igual + 1
                            break #paro a execução se achar igual
                if(len(metodo[2]) == qtd_igual):
                    return False
    return True

def imprimeErroMetodo(item):
    global erros

    erros.append("Erro encontrado na linha "+item[0]+". Já existe Metodo "+item[1]+" e parametros "+item[2]+".")

def analisaResultado(tokens, tipo_metodo, variaveis):
    token = tokens.pop(0)
    [linha, tipo, valor] = token
    if(tipo == 'IDE'):
        variavel = getItem(variaveis, ['', '', valor])
        if(not variavel):
            imprimeErroVariavel(2, [linha, '', valor])
        elif(variavel[2] != tipo_metodo):
            erros.append('Erro encontrado na linha: '+linha+'. Retorno esperado '+listaMetodos[num_metodo][3])
        # elif(variavel[]):
        #     pass

#Leia -----------------------------------
def analisaLeia(tokens, listaVariaveis):

    while len(tokens)>0:
        token = tokens.pop(0)
        [linha, tipo, valor] = token
        if(tipo == 'IDE'):
            if(not getItem(listaVariaveis, ['', '', valor])):
                imprimeErroVariavel(2, [linha, '', valor])

#---------------------------------------------------------------------------------
#Escreva -------------------------------------------
def analisaEscreva(tokens, variaveis):
    cadeia = False
    while len(tokens)>0:
        token = tokens.pop(0)
        [linha, tipo, valor] = token
        
        if(tipo == 'IDE'):
            variavel = getItem(variaveis, ['', '', valor])
            if(not variavel):
                imprimeErroVariavel(2, [linha, '', valor])
            elif(cadeia and variavel[1] != 'CAD'):
                imprimeErroVariavel(3, [linha, 'texto', valor])
        elif(tipo == 'CAD'):
            cadeia = True
        elif(cadeia and valor == ',\n' or valor == ')\n'):
            cadeia = False     
            
#---------------------------------------------------------------------------------
#Metodos Genéricos -------------------------------------------
def separaBloco(tokens):
    bloco = [] #Bloco do metodo contendo todo o corpo do metodo
    pilha = [] #Empilho quando ouver uma abertura de bloco

    fim_bloco = False

    while not fim_bloco:        
        token = ''
        token = tokens.pop(0)        
        [linha, tipo, valor] = token

        if(valor == '{\n'):
            pilha.append(valor)
        elif(valor == '}\n'):
            pilha.pop(0)
        
        if(len(pilha)<=0):
            fim_bloco = True
        
        bloco.append(token)
    return bloco
    
def mapeiaDeclaracao(listaApend, tokens):
    tipo_atual = ''
    vetor = 0    
    item_tabela = []
    while len(tokens)>0:

        token = tokens.pop(0)        
        [linha, tipo, valor] = token
        if(tipo == 'PRE'):
            if(valor != 'verdadeiro\n' and valor != 'falso\n'):
                tipo_atual = valor
            elif(tipo_atual != 'booleano\n'):
                imprimeErroConstante(1, [linha, tipo_atual])
        elif(tipo == 'IDE'):
            item_tabela.append(linha)
            item_tabela.append(tipo_atual)
            item_tabela.append(valor)
        elif(tipo == 'CAD'):
            if(tipo_atual != 'texto\n'):
                imprimeErroConstante(1, [linha, tipo_atual])
        elif(tipo == 'NRO'):
            if(tipo_atual != 'real\n' and tipo_atual != 'inteiro\n'):
                imprimeErroConstante(1, [linha, tipo_atual])
            if(tipo_atual == 'inteiro\n' and '.' in valor):                
                imprimeErroConstante(1, [linha, tipo_atual])
        elif(valor == '[\n'):
            vetor = vetor + 1
            if(vetor == 1):
                item_tabela.append('vetor')
            elif(vetor == 2):
                item_tabela[3] = 'matriz'
            while valor != ']\n':
                token = tokens.pop(0)
                [linha, tipo, valor] = token

                if(tipo == 'NRO' and '.' not in valor):
                    item_tabela.append(valor)
        elif(valor == ',\n' or valor == ';\n'):
            if(getItem(listaApend, item_tabela)):
                imprimeErroConstante(0, item_tabela)
            else:
                listaApend.append(item_tabela)
                ultimaConstante = item_tabela
                item_tabela = []

def getItem(lista, value):
    for item in lista:
        if(value[2] == item[2]): #verifica se nome é igual
            return item
    
    return False

def validaAtribuicao(destino, expressao): #Expressao será um array de tokens do lado direito do =
    global erros
    tipo_destino = destino[1]
    if(tipo_destino == 'vazio\n' and expressao[0][2] != 'vazio\n'):
        erros.append("Erro encontrado na linha "+expressao[0][0]+". Esperava retorno do tipo "+tipo_destino)
    elif(tipo_destino == 'inteiro\n' or tipo_destino == 'real\n'):
        pass
    elif(tipo_destino == 'texto\n'):
        pass
    elif(tipo_destino == 'boleano\n'):
        pass