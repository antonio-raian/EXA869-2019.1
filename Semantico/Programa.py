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
    #tokens = lista_tokens.copy()
    #Nesse ponto os tokens não possuem mais as constantes e a tabela de constantes está preenchida
    analisaMetodos(tokens)
    print (erros)
    return erros
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
    while len(tokens) > 0:
        token = ''
        token = tokens.pop(0)
        if(token[2]=='metodo\n'):            
            num_metodo = num_metodo + 1
            tabela_variaveis = []
            mapeiaMetodo(tokens)
            #Nesse ponto aq os tokens não possuem mais a declaração do metodo e o topo é {
            bloco_metodo = separaBloco(tokens)
            #Nesse ponto os tokens não possuem mais o metodo em analise, o metodo está em bloco metodo
            validaCorpoMetodo(bloco_metodo, tabela_variaveis, num_metodo)
        elif(token[2] == 'principal\n'):
            num_metodo = num_metodo + 1
            tabela_variaveis = []
            listaMetodos.append([token[0], 'principal\n', [], 'vazio\n'])
            #Nesse ponto aq os tokens não possuem mais a declaração do metodo e o topo é {
            bloco_principal = separaBloco(tokens)
            #Nesse ponto os tokens não possuem mais o metodo em analise, o metodo está em bloco metodo
            validaCorpoMetodo(bloco_principal, tabela_variaveis, num_metodo)

def validaCorpoMetodo(tokens, variaveis, num):    
    global listaMetodos
    global erros

    while len(tokens)>0:
        token = tokens.pop(0)
        [linha, tipo, valor] = token
        if(valor == 'variaveis\n'):
            bloco_variaveis = separaBloco(tokens) 
            mapeiaDeclaracao(variaveis, bloco_variaveis) #No fim a tabela de variaveis deve estar preenchida
        elif(tipo == 'PRE'):
            if(valor == 'leia\n'):
                inst_leia = []
                while valor != ';\n':
                    token = tokens.pop(0)
                    [linha, tipo, valor] = token                            
                    inst_leia.append(token) #Ao fim o inst_leia será a instrução sem o 'leia'
                analisaLeia(inst_leia, variaveis)
            elif(valor == 'escreva\n'):
                inst_escreva = []
                while valor != ';\n':
                    token = tokens.pop(0)
                    [linha, tipo, valor] = token                            
                    inst_escreva.append(token) #Ao fim o inst_escreva será a instrução sem o 'escreva'
                analisaEscreva(inst_escreva, variaveis)
            elif(valor == 'se\n'):
                exp_se = []
                while valor != 'entao\n':
                    token = tokens.pop(0)
                    [linha, tipo, valor] = token                            
                    exp_se.append(token) #Ao fim o exp_se será a expressao do se
                analisaLog(exp_se, variaveis, 'boleano\n')
                #Nesse ponto tokens não terá mais a declaração do se
                bloco_se = separaBloco(tokens)
                validaCorpoMetodo(bloco_se, variaveis, num)
            elif(valor == 'senao\n'):
                bloco_senao = separaBloco(tokens)
                validaCorpoMetodo(bloco_senao, variaveis, num)
            elif(valor == 'enquanto\n'):
                exp_enquanto = []
                while valor != 'entao\n':
                    token = tokens.pop(0)
                    [linha, tipo, valor] = token                            
                    exp_enquanto.append(token) #Ao fim o exp_enquanto será a expressao do enquanto
                analisaLog(exp_enquanto, variaveis, 'boleano\n')
                #Nesse ponto tokens não terá mais a declaração do enquanto
                bloco_enquanto = separaBloco(tokens)
                validaCorpoMetodo(bloco_enquanto, variaveis, num)
            elif(valor == 'resultado\n'):
                exp = []
                while valor != ';\n':
                    token = tokens.pop(0)
                    [linha, tipo, valor] = token
                    exp.append(token)

                validaAtribuicao(['', listaMetodos[num][2], ''], exp, variaveis)
        elif(tipo == 'IDE'):
            var_aux = valor
            var = getItem(variaveis, token)
            const = getItem(tabelaConstantes, token)
            metod = getMetodo(token)

            exp = []
            while valor != ';\n':
                token = tokens.pop(0)
                [linha, tipo, valor] = token
                exp.append(token)
            if(var):
                exp.pop(0) #Só pra remover o =
                validaAtribuicao(var, exp, variaveis)
            elif(const):
                erros.append("Erro encontrado na linha "+linha+". "+var_aux+' é constante!')
            elif(metod):
                validaChamadaMetodo(metod, exp, variaveis)
            else:
                erros.append("Erro encontrado na linha "+linha+". "+var_aux+' não encontrado (a)!')

def mapeiaMetodo(tokens):
    global listaMetodos

    fim_declaracao = False
    in_parametros = False
    parametros = []
    item_parametro = []
    item_tabela = []
    while not fim_declaracao:
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
                item_tabela.append(parametros)
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
                item_tabela = []
            else:
                imprimeErroMetodo(item_tabela)
            fim_declaracao = True

def validaChamadaMetodo(metodo, exp, variaveis):
    global erros
    params = 0
    while len(exp)>0:
        token = exp.pop(0)
        [linha, tipo, valor] = token

        if(tipo == 'IDE'):
            var = varOuConstTipo(variaveis, token, [metodo[2][params][0]])
            if(not var):
                erros.append("Erro encontrado na linha "+linha+". "+valor+' não encontrado (a)!')
            params = params + 1
    
    if(params != len(metodo[2])):
        erros.append("Erro encontrado na linha "+linha+". Quantidade de parametros incompativel!")
        
        

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

def getMetodo(token):
    global listaMetodos

    for metodo in listaMetodos:
        if(metodo[1] == token[2]):
            return metodo
    return False

def imprimeErroMetodo(item):
    global erros

    erros.append("Erro encontrado na linha "+item[0]+". Já existe Metodo "+item[1]+" e parametros "+item[2]+".")

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
            elif(tipo_atual != 'boleano\n'):
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

def validaAtribuicao(destino, expressao, variaveis): #Expressao será um array de tokens do lado direito do =
    global erros
    global tabelaConstantes

    tipo_destino = destino[1]
    tipo_expressao = tipoExpressao(expressao)
    if(tipo_destino == 'vazio\n' and expressao[0][2] != 'vazio\n'):
        erros.append("Erro encontrado na linha "+expressao[0][0]+". Esperava retorno do tipo "+tipo_destino)
        return
    elif(tipo_destino == 'inteiro\n' or tipo_destino == 'real\n'):
        if(len(tipo_expressao)>1):
            erros.append("Erro encontrado na linha "+expressao[0][0]+". Atribuindo uma expressão lógica incorretamente!")
        elif(tipo_expressao[0]=='var'):
            varOuConstTipo(variaveis, expressao[0], [tipo_destino])
        elif(tipo_expressao[0]=='num'):
            if(tipo_destino == 'inteiro\n' and '.' in expressao[0][2]):
                erros.append("Erro encontrado na linha "+expressao[0][0]+". Esperava atribuição do tipo "+tipo_destino+', recebeu do tipo real')
        elif(tipo_expressao[0] == 'ari'):
            while len(expressao)>0:
                token = expressao.pop(0)
                [linha, tipo, valor] = token
                if(tipo == 'IDE'):
                    if(tipo_destino == 'inteiro\n'):
                        varOuConstTipo(variaveis, token, [tipo_destino])
                    else:
                        var = varOuConstTipo(variaveis, token, ['inteiro\n', 'real\n'])
                        tipo_var = var[1] if var else var
                        if(tipo_var and (tipo_var != 'inteiro\n' or tipo_var != 'real\n')):
                            erros.append("Erro encontrado na linha "+token[0]+". Esperava atribuição do tipo real ou inteiro, recebeu do tipo "+tipo_var)
                elif(tipo == 'NRO'):
                    if(tipo_destino == 'inteiro\n' and '.' in expressao[0][2]):
                        erros.append("Erro encontrado na linha "+token[0]+". Esperava atribuição do tipo "+tipo_destino+', recebeu do tipo real')
        elif(tipo_expressao[0] == 'log'):
            analisaLog(expressao, variaveis)
    elif(tipo_destino == 'texto\n'):
        pass #A gramatica não permite atribuir texto só em constantes
    elif(tipo_destino == 'boleano\n'):
        pass
    
def analisaLog(expressao, variaveis, tipo_destino):
    global tabelaConstantes
    global erros
    auxlog1 = ""
    auxlog2 = ""

    while len(expressao)>0:
        token = expressao.pop(0)
        [linha, tipo, valor] = token
        if(tipo_destino != 'boleano\n'):
            erros.append("Erro encontrado na linha "+token[0]+". Atribuicao de expressão relacional ou lógica para variável de tipo não-boleano.")
        elif(tipo == 'IDE' and auxlog1 == ""):
            varlog = getItem(variaveis, token)

            if not varlog:
                varlog = getItem(tabelaConstantes, token)
                if not varlog:
                    erros.append("Erro encontrado na linha "+token[0]+". "+token[2]+' Não foi declarado!')
                else:
                    auxlog1 = varlog[1]
            else:
                auxlog1 = varlog[1]
        elif(tipo == 'IDE' and auxlog1 != ""):
            varlog2 = getItem(variaveis, token)

            if not varlog2:
                varlog2 = getItem(tabelaConstantes, token)
                if not varlog2:
                    erros.append("Erro encontrado na linha "+token[0]+". "+token[2]+' Não foi declarado!')
                else:
                    auxlog2 = varlog2[1]
            else:
                auxlog2 = varlog2[1]

                if auxlog1 != auxlog2:
                    erros.append("Erro encontrado na linha "+token[0]+". "+token[2]+' Operação lógica/relacional entre variáveis de tipos diferentes!')
                auxlog1 = ""
                auxlog2 = ""
        elif(tipo == 'PRE'):
            if (valor != 'verdadeiro\n' and valor != 'falso\n'):
                erros.append("Erro encontrado na linha "+token[0]+". Esperava atribuição do tipo boleano, encontrou atribuicao de palavra reservada.")
        elif(tipo == 'NRO' and auxlog1 == ""):
            auxlog1 == 'inteiro\n'
        elif(tipo == 'NRO' and auxlog1 != ""):
            if (auxlog1 != 'inteiro\n' and auxlog1 != 'real\n'):
                erros.append("Erro encontrado na linha "+token[0]+". Operação lógica/relacional entre variáveis de tipos diferentes! ")

        else:
            erros.append("Erro encontrado na linha "+token[0]+". Esperava atribuição do tipo boleano, encontrou atribuicao desconhecida.")

def tipoExpressao(tokens):
    tipo_expressao = ['nada']
    pos = 0

    for token in tokens:
        [linha, tipo, valor] = token
        if(tipo == 'IDE' and tipo_expressao[pos] == 'nada'):
            tipo_expressao[pos] = 'var'
        elif(tipo == 'ARI'):
            tipo_expressao[pos] = 'ari'
        elif(tipo == 'LOG'):
            tipo_expressao[pos] = 'log'
            pos = pos + 1
            tipo_expressao.append('nada')
        elif(tipo == 'REL'):
            tipo_expressao[pos] = 'log'
        elif(tipo == 'NRO' and tipo_expressao[pos] == 'nada'):
            tipo_expressao[pos] = 'num'

    return tipo_expressao

def varOuConstTipo(variaveis, token, tipo_destino):
    global tabelaConstantes

    var = getItem(variaveis, token)
    if(var):
        if(var[1] not in tipo_destino):
            erros.append("Erro encontrado na linha "+token[0]+". Esperava atribuição do tipo ".join(tipo_destino)+', recebeu do tipo '+var[1])
        return var
    else:
        const = getItem(tabelaConstantes, token)
        if(const):
            if(var[1] not in tipo_destino):
                erros.append("Erro encontrado na linha "+token[0]+". Esperava atribuição do tipo ".join(tipo_destino)+', recebeu do tipo '+var[1])
            return const
        else:
            erros.append("Erro encontrado na linha "+token[0]+". "+token[2]+' Não foi declarado!')
    return False
