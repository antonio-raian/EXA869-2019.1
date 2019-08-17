tokens = ""
erros = ""

def main(lista_tokens):
    global tokens
    tokens = lista_tokens

    print(lista_tokens)
    for token in lista_tokens:
        n_linha = token[0]
        tipo = token[1]
        value = token[2]
        print('LINHA '+n_linha+ '->TIPO '+tipo+'->VALOR '+value)

    analisa_programa()    




def analisa_programa():
	global tokens
	backup = tokens

	esperado = "programa\n"

	if tokens[1][2] == esperado
		tokens = tokens[1:] #<- AVANÇA PARA O PROXIMO

		esperado = "{\n"

		if tokens[1][2] == esperado
			tokens = tokens[1:]

			analisa_corpo_code():

			esperado = "}\n"

			if tokens[1][2] == esperado
				tokens = tokens[1:]

				return true
	return false				


def analisa_corpo_code():
	global tokens
	backup = tokens

	analisa_constantes():
	analisa_bloco_de_metodos():
	analisa_principal():
	
	return true


def analisa_constantes():
	global tokens
	backup = tokens

	esperado = "constantes\n"

	if tokens[1][2] == esperado
		tokens = tokens[1:]

		esperado = "{\n"

		if tokens[1][2] == esperado
			tokens = tokens[1:]

			analisa_corpo_constantes():

			esperado = "}\n"

			if tokens[1][2] == esperado
				tokens = tokens[1:]

				return true
	return false			


def analisa_corpo_constantes():		#ACEITA VAZIO. PORTANTO, DEVE PODER RETORNAR AO BACKUP CASO ENCONTRE ERRO.		
	global tokens
	backup = tokens

	analisa_tipo():
	esperado = "IDE"

	if tokens[1][1] == esperado:
		tokens = tokens[1:]

		esperado = "=\n"
		if tokens[1][2] == esperado:
			tokens = tokens[1:]

			analisa_valor_atribuido():

			analisa_prox_declaracao_constantes():

			return true
	#SE ALGUMA DAS CONDICOES NAO FOR VERDADEIRA

	tokens = backup
	return true						

def analisa_prox_declaracao_constantes():
	global tokens
	backup = tokens

	if tokens[1][2] == ";\n":
		tokens = tokens[1:]

		analisa_corpo_constantes()

		return true

	elif tokens[1][2] == ",\n":

		esperado = "IDE"

		if tokens[1][1] == esperado:
			tokens = tokens[1:]

			esperado = "=\n"

			if tokens[1][2] == esperado:
				tokens = tokens[1:]

				analisa_valor_atribuido()
				analisa_prox_declaracao_constantes()

				return true

	return false			

def analisa_tipo():
	global tokens
	backup = tokens

	if (tokens[1][2] == "inteiro\n") or (tokens[1][2] == "real\n") or (tokens[1][2] == "texto\n") or (tokens[1][2] == "boleano\n"):
		tokens = tokens[1:]

		return true
	else:
		return false

def analisa_valor_atribuido():
	global tokens
	backup = tokens

	if analisa_boleano():
		tokens = tokens[1:]

		return true
	elif (tokens[1][1] == "CAD") or (tokens[1][1] == "NRO"):
		tokens = tokens[1:]

		return true
	else:
		return false	


def analisa_boleano():
	global tokens
	backup = tokens

	if (tokens[1][2] == "verdadeiro\n") or (tokens[1][2] == "falso\n"):
		tokens = tokens[1:]

		return true
	else:
		return false

def analisa_bloco_de_metodos():


def analisa_corpo_metodo():

def analisa_bloco_de_variaveis():

def analisa_comandos():

def analisa_corpo_variavel():

def analisa_variavel():

def analisa_prox_declaracao():

def analisa_extensao_vetor():

def analisa_extensao_matriz():

def analisa_id_ou_num():

def analisa_comandos_aux():

def analisa_leia():

def analisa_leitura():

def analisa_leitura_aux():

def analisa_escreva():

def analisa_impresso():

def analisa_impresso_aux():

def analisa_exp_cadeia():

def analisa_exp_cadeia_aux():	

def analisa_atribuicao():

def analisa_atribuiveis():

def analisa_expressoes():

def analisa_lacos():

def analisa_condicionais():

def analisa_condicional_else():

def analisa_chamada_de_metodo():

def analisa_parametro_chamada():

def analisa_parametro_chamada_aux():

def analisa_principal():

def analisa_metodos():

def analisa_resultado_do_metodo():

def analisa_tipo_retorno():

def analisa_parametro():

def analisa_parametro_aux():

def analisa_operador_relacional():

def analisa_op_logico():

def analisa_exp_soma():

def analisa_exp_art_aux():

def analisa_sinal1():

def analisa_exp_mul():

def analisa_exp_art_aux2():

def analisa_sinal2():

def analisa_exp_parenteses():

def analisa_exp_relacional():

def analisa_exp_relacional_not():

def analisa_boleano_aux_1():  

def analisa_boleano_aux_2():

def analisa_boleano_aux():   

def analisa_exp_logica_aux():

def analisa_exp_logica_aux_3():

def analisa_exp_logica_aux_2():

def analisa_exp_logica():

def analisa_exp_logica_recurrency():