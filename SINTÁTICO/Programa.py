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

	if (tokens[1][2] == esperado):
		tokens = tokens[1:] #<- AVANÇA PARA O PROXIMO

		esperado = "{\n"

		if tokens[1][2] == esperado:
			tokens = tokens[1:]

			analisa_corpo_code()

			esperado = "}\n"

			if tokens[1][2] == esperado:
				tokens = tokens[1:]

				return True
	return False				


def analisa_corpo_code():
	global tokens
	backup = tokens

	analisa_constantes()
	analisa_bloco_de_metodos()
	analisa_principal()
	
	return True


def analisa_constantes():
	global tokens
	backup = tokens

	esperado = "constantes\n"

	if tokens[1][2] == esperado:
		tokens = tokens[1:]

		esperado = "{\n"

		if tokens[1][2] == esperado:
			tokens = tokens[1:]

			analisa_corpo_constantes()

			esperado = "}\n"

			if tokens[1][2] == esperado:
				tokens = tokens[1:]

				return True
	return False			


def analisa_corpo_constantes():		#ACEITA VAZIO. PORTANTO, DEVE PODER RETORNAR AO BACKUP CASO ENCONTRE ERRO.		
	global tokens
	backup = tokens

	analisa_tipo()
	esperado = "IDE"

	if tokens[1][1] == esperado:
		tokens = tokens[1:]

		esperado = "=\n"
		if tokens[1][2] == esperado:
			tokens = tokens[1:]

			analisa_valor_atribuido()

			analisa_prox_declaracao_constantes()

			return True
	#SE ALGUMA DAS CONDICOES NAO FOR VERDADEIRA

	tokens = backup
	return True						

def analisa_prox_declaracao_constantes():
	global tokens
	backup = tokens

	if tokens[1][2] == ";\n":
		tokens = tokens[1:]

		analisa_corpo_constantes()

		return True

	elif tokens[1][2] == ",\n":

		esperado = "IDE"

		if tokens[1][1] == esperado:
			tokens = tokens[1:]

			esperado = "=\n"

			if tokens[1][2] == esperado:
				tokens = tokens[1:]

				analisa_valor_atribuido()
				analisa_prox_declaracao_constantes()

				return True

	return False			

def analisa_tipo():
	global tokens
	backup = tokens

	if (tokens[1][2] == "inteiro\n") or (tokens[1][2] == "real\n") or (tokens[1][2] == "texto\n") or (tokens[1][2] == "boleano\n"):
		tokens = tokens[1:]

		return True
	else:
		return False

def analisa_valor_atribuido():
	global tokens
	backup = tokens

	if analisa_boleano():
		tokens = tokens[1:]

		return True
	elif (tokens[1][1] == "CAD") or (tokens[1][1] == "NRO"):
		tokens = tokens[1:]

		return True
	else:
		return False	


def analisa_boleano():
	global tokens
	backup = tokens

	if (tokens[1][2] == "verdadeiro\n") or (tokens[1][2] == "falso\n"):
		tokens = tokens[1:]

		return True
	else:
		return False

def analisa_bloco_de_metodos():
	return True
def analisa_corpo_metodo():
	return True
def analisa_bloco_de_variaveis():
	return True
def analisa_comandos():
	return True
def analisa_corpo_variavel():
	return True
def analisa_variavel():
	return True
def analisa_prox_declaracao():
	return True
def analisa_extensao_vetor():
	return True
def analisa_extensao_matriz():
	return True
def analisa_id_ou_num():
	global tokens
	if(tokens[1][1] =='IDE\n' or tokens[1][1]=='NRO'):
		return True
	return False

def analisa_comandos_aux():
	return True

def analisa_leia():
	return True

def analisa_leitura():
	return True

def analisa_leitura_aux():
	return True

def analisa_escreva():
	global tokens
	if(tokens[1][2] == 'escreva\n'):
		tokens = tokens[1:]
		if(tokens[1][2] == '(\n'):
			tokens = tokens[1:]
			analisa_impresso()
			analisa_impresso_aux()
			if(tokens[1][2] == ')\n'):
				tokens = tokens[1:]
				if(tokens[1][2] == ';\n'):
					tokens = tokens[1:]
					return True
				else:
					return False
			else:
				return False
		else:
			return False
	else:
		return False

def analisa_impresso():
	return analisa_variavel() or analisa_exp_cadeia()

def analisa_impresso_aux():
	global tokens
	if(tokens[1][2]==',\n'):
		tokens = tokens[1:]
		return (analisa_impresso() and analisa_impresso_aux())
	return True 

def analisa_exp_cadeia():
	global tokens
	if(tokens[1][1 == 'CAD\n']):
		tokens = tokens[1:]
		return analisa_exp_cadeia_aux()
	else:
		return False

def analisa_exp_cadeia_aux():
	global tokens
	if(tokens[1][2]=='+\n'):
		tokens = tokens[1:]
		if(tokens[1][1] == 'CAD\n'):
			tokens = tokens[1:]
	return True

def analisa_atribuicao():
	global tokens
	analisa_variavel()
	if(tokens[1][2]=='='):
		tokens = tokens[1:]
		analisa_atribuiveis()
		if(tokens[1][2]==';'):
			tokens = tokens[1:]
			return True
		else:
			return False
	else:
		return False

def analisa_atribuiveis():
	global tokens
	if(tokens[1][2]=='vazio\n' or tokens[1][1]=='NRO\n'):
		return True
	else:
		return analisa_expressoes() or analisa_boleano()
	return True

def analisa_expressoes():
	return analisa_exp_soma() or analisa_exp_relacional() or analisa_exp_logica()

def analisa_lacos():
	global tokens
	if(tokens[1][2] == 'enquanto\n'):
		tokens = tokens[1:]
		analisa_exp_logica()
		if(tokens[1][2] == 'entao\n'):
			tokens = tokens[1:]
			if(tokens[1][2] == '{\n'):
				tokens = tokens[1:]
				analisa_corpo_metodo()
				if(tokens[1][2] == '}\n'):
					tokens = tokens[1:]
					return True
				else:
					return False
			else:
				return False
		else:
			return False
	else:
		return False

def analisa_condicionais():
	global tokens
	if(tokens[1][2] == 'se\n'):
		tokens = tokens[1:]
		analisa_exp_logica()
		if(tokens[1][2] == 'entao\n'):
			tokens = tokens[1:]
			if(tokens[1][2] == '{\n'):
				tokens = tokens[1:]
				analisa_corpo_metodo()
				if(tokens[1][2] == '}\n'):
					tokens = tokens[1:]
					return analisa_condicional_else()
				else:
					return False
			else:
				return False
		else:
			return False
	else:
		return False

def analisa_condicional_else():
	global tokens
	if(tokens[1][2] == 'senao\n'):
		tokens = tokens[1:]
		if(tokens[1][2] == '{\n'):
			tokens = tokens[1:]
			analisa_corpo_metodo()
			if(tokens[1][2]=='}\n'):
				tokens = tokens[1:]
				return True
			else:
				return False
		else:
			return False
	return True

def analisa_chamada_de_metodo():
	global tokens
	if(tokens[1][1] == 'IDE\n'):
		tokens = tokens[1:]
		if(tokens[1][2] == '(\n'):
			tokens = tokens[1:]
			analisa_parametro_chamada()
			if(tokens[1][2] == ')\n'):
				tokens = tokens[1:]
				if(tokens[1][2] == ';\n'):
					tokens = tokens[1:]
					return True
				else:
					return False
			else:
				return False
		else:
			return False
	else:
		return False

def analisa_parametro_chamada():
	return analisa_variavel() and analisa_parametro_chamada_aux()

def analisa_parametro_chamada_aux():
	global tokens
	if(tokens[1][2] == ',\n'):
		tokens = tokens[1:]
		return analisa_parametro_chamada()
	else:
		return True

def analisa_principal():
	global tokens
	if(tokens[1][2] == 'principal\n'):
		tokens = tokens[1:]
		if(tokens[1][2] == '{\n'):
			tokens = tokens[1:]
			analisa_corpo_metodo()
			if(tokens[1][2] == '}\n'):
				tokens = tokens[1:]
				return True
			else:
				return False
		else:
			return False
	else:
		return False

def analisa_metodos():
	global tokens
	if(tokens[1][2] == 'metodo\n'):
		tokens = tokens[1:]
		if(tokens[1][1] == 'IDE\n'):
			tokens = tokens[1:]
			if(tokens[1][2] == '(\n'):
				tokens = tokens[1:]
				analisa_parametro()
				if(tokens[1][2] == ')\n'):
					tokens = tokens[1:]
					if(tokens[1][2] == ':\n'):
						tokens = tokens[1:]
						analisa_tipo_retorno()
						if(tokens[1][2] == '{\n'):
							tokens = tokens[1:]
							analisa_corpo_metodo()
							if(tokens[1][2] == '}\n'):
								tokens = tokens[1:]
								return analisa_metodos()
							else:
								return False
						else:
							return False
					else:
						return False
				else:
					return False
			else:
				return False
		else:
			return False
	return True

def analisa_resultado_do_metodo():
	global tokens
	if(tokens[1][2]== 'vazio\n'):
		tokens = tokens[1:]
		return True
	else:
		return analisa_variavel()

def analisa_tipo_retorno():
	global tokens
	if(tokens [1][1] == 'CAD\n' or tokens[1][1]=='NRO\n' or tokens[1][2]=='vazio\n'):
		tokens = tokens[1:]
		return True
	else:
		return analisa_boleano()

def analisa_parametro():
	global tokens
	analisa_tipo()
	if(token[1][1]=='IDE\n'):
		return analisa_parametro_aux()
	else:
		return False

def analisa_parametro_aux():
	global tokens
	if(tokens[1][2]==',\n'):
		tokens = tokens[1:]
		return analisa_parametro()
	else:
		return True

def analisa_operador_relacional():
	global tokens
	if(tokens[1][2] == '!=\n' or tokens[1][2] == '==\n' or tokens[1][2] ==  '<\n' or tokens[1][2] == '>\n' or tokens[1][2] ==  '<=\n' or tokens[1][2] ==  '>=\n' or tokens[1][2] ==  '=\n'):
		tokens = tokens[1:]
		return True
	return False

def analisa_op_logico():
	global tokens
	if(tokens[1][2] == '&&\n') or (tokens[1][2] == '||\n'):
		tokens = tokens[1:]
		return True
	return False

def analisa_exp_soma():
	return analisa_exp_mul() and analisa_exp_art_aux()

def analisa_exp_art_aux():
	global tokens
	if(tokens[1][2] == '++\n' or tokens[1][2] == '--\n'):
		tokens = tokens[1:]
		return True
	else:
		return (analisa_sinal1() and analisa_exp_soma()) or True

def analisa_sinal1():
	global tokens
	if(tokens[1][2] == '+\n' or tokens[1][2] == '-\n'):
		tokens = tokens[1:]
		return True
	return False

def analisa_exp_mul():
	return analisa_exp_parenteses() and analisa_exp_art_aux2()

def analisa_exp_art_aux2():
	return (analisa_sinal2() and analisa_exp_mul()) or True

def analisa_sinal2():
	global tokens
	if(tokens[1][2] == '*\n' or tokens[1][2 == '/\n']):
		tokens = tokens[1:]
		return True
	return False

def analisa_exp_parenteses():
	global tokens
	if(tokens[1][2] == '(\n'):
		tokens = tokens[1:]
		analisa_expressoes()
		if(tokens[1][2]==')\n'):
			tokens = tokens[1:]
			return True
	elif (tokens[1][1]=='NRO\n'):
		tokens = tokens[1:]
		return True
	else:
		return analisa_variavel()

	return False
	
def analisa_exp_relacional():
	return analisa_id_ou_num() and analisa_operador_relacional() and analisa_id_ou_num()

def analisa_exp_relacional_not():
	global tokens
	if( tokens[1][2] == '!\n' ):
		tokens = tokens[1:]
	return analisa_exp_relacional()
	return True

def analisa_boleano_aux_1():
	global tokens
	if( tokens[1][2] == '!\n' ):
		tokens = tokens[1:]
	return analisa_boleano()

def analisa_boleano_aux_2():
	global tokens
	if( tokens[1][2] == '!\n' ):
		tokens = tokens[1:]
	return analisa_variavel()

def analisa_boleano_aux():   
	return analisa_boleano_aux_1() or analisa_boleano_aux_2()

def analisa_exp_logica_aux():
	global tokens
	if (tokens[1][2] == "!\n") or (tokens[1][2] == "(\n"):
		tokens = tokens[1:]
		if (tokens[1][2] == "(\n"):
			tokens = tokens[1:]

	analisa_exp_logica_aux_2()

	if(tokens[1][2] == ")\n"):
		tokens = tokens[1:]

	return True

def analisa_exp_logica_aux_3():
	return analisa_boleano_aux() or analisa_exp_relacional_not()

def analisa_exp_logica_aux_2():
	return analisa_exp_logica_aux_3() and analisa_op_logico() and analisa_exp_logica_aux_3()

def analisa_exp_logica():	
	return analisa_exp_logica_aux() and analisa_exp_logica_recurrency()

def analisa_exp_logica_recurrency():
	return (analisa_op_logico() and analisa_exp_logica()) or True