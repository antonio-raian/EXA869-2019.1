import sys
import os

file = ""
tokens = ""
erros = ""
output = ''

def main(lista_tokens, arq):
	global tokens
	global file
	global output

	tokens = lista_tokens
	file = arq
	diretorioSaida = os.path.abspath('.')+"/saida_sintatico/"
	if(not os.path.isdir(diretorioSaida)):
		os.mkdir(diretorioSaida)
	
	output = open(diretorioSaida +file, 'w')
	
	result = analisa_programa()    
	
	output.close()
	return result

def analisa_programa():
	global tokens
	backup = tokens

	esperado = "programa\n"

	if (tokens[0][2] == esperado):
		tokens = tokens[1:] #<- AVANÇA PARA O PROXIMO

		esperado = "{\n"

		if tokens[0][2] == esperado:
			tokens = tokens[1:]
			if(analisa_corpo_code()):
				esperado = "}\n"
				if tokens[0][2] == esperado:
					#tokens = tokens[1:]
					# print(tokens[0])
					return True

				else:
					salva_erro("}")
		else:
			salva_erro("{")
	else:
		salva_erro("programa")
	return False				

def analisa_corpo_code():
	global tokens
	backup = tokens

	#print(tokens[0])
	if(analisa_constantes()):
		print(tokens[0])
		if(analisa_metodos()):
			print(tokens[0])
			if(analisa_principal()):
				return True
	#print(tokens[0])
	
	return False

def analisa_constantes():
	global tokens
	backup = tokens

	esperado = "constantes\n"

	if tokens[0][2] == esperado:
		tokens = tokens[1:]
		esperado = "{\n"
		if tokens[0][2] == esperado:
			tokens = tokens[1:]
			esperado = "}\n"
			if tokens[0][2] == esperado:
				tokens = tokens[1:]				
				return True
			else:
				if(analisa_corpo_constantes()):
					if tokens[0][2] == esperado:
						tokens = tokens[1:]				
						return True

					else:
						salva_erro("}")
		else:
			salva_erro("{")
	else:
		salva_erro("constantes")
				
	return False			

def analisa_corpo_constantes():		#ACEITA VAZIO. PORTANTO, DEVE PODER RETORNAR AO BACKUP CASO ENCONTRE ERRO.		
	global tokens
	backup = tokens

	if(analisa_tipo()):
		esperado = "IDE"

		if tokens[0][1] == esperado:
			tokens = tokens[1:]

			esperado = "=\n"
			if tokens[0][2] == esperado:
				tokens = tokens[1:]

				analisa_valor_atribuido()

				analisa_prox_declaracao_constantes()

				return True
			else:
				salva_erro('=')
		#SE ALGUMA DAS CONDICOES NAO FOR VERDADEIRA

		tokens = backup
		return True						
	else:
		salva_erro("inteiro, real, texto ou boleano")
		return False

def analisa_prox_declaracao_constantes():
	global tokens
	backup = tokens
	#print(tokens[0])
	if tokens[0][2] == ";\n":
		tokens = tokens[1:]
		if(tokens[0][2] != '}\n'):
			analisa_corpo_constantes()

		return True

	elif tokens[0][2] == ",\n":
		tokens = tokens[1:]
		esperado = "IDE"

		if tokens[0][1] == esperado:
			tokens = tokens[1:]

			esperado = "=\n"

			if tokens[0][2] == esperado:
				tokens = tokens[1:]

				analisa_valor_atribuido()
				analisa_prox_declaracao_constantes()

				return True
			else:
				salva_erro("=")
		else:
			salva_erro("nome da constante")
	else:
		salva_erro("; ou ,")

	return False			

def analisa_tipo():
	global tokens
	backup = tokens
	if(tokens[0][1] =='PRE'):
		if (tokens[0][2] == "inteiro\n") or (tokens[0][2] == "real\n") or (tokens[0][2] == "texto\n") or (tokens[0][2] == "boleano\n"):
			tokens = tokens[1:]

			return True
		else:
			# salva_erro("inteiro, real, texto ou boleano")
			return False
	else:
		return False

def analisa_valor_atribuido():
	global tokens
	backup = tokens

	if analisa_boleano():

		return True
	elif (tokens[0][1] == "CAD") or (tokens[0][1] == "NRO"):
		tokens = tokens[1:]
		#print(tokens[0])

		return True
	else:
		salva_erro("verdadeiro, falso, CAD ou NRO")
		return False	


def analisa_boleano():
	global tokens
	backup = tokens

	if (tokens[0][2] == "verdadeiro\n") or (tokens[0][2] == "falso\n"):
		tokens = tokens[1:]

		return True
	else:
		return False


def analisa_corpo_metodo(): 
	global tokens
	backup = tokens

	if(analisa_bloco_de_variaveis()):
		#print(tokens[0])
		analisa_comandos()
		#print(tokens[0])
		if (tokens[0][2]=='resultado\n'):
			tokens = tokens[1:]

			analisa_resultado_do_metodo()

			if (tokens[0][2] == ';\n'):
				tokens = tokens[1:]

				return True
			else:
				salva_erro(";")
		else:
			salva_erro("resultado")
	
	return False

def analisa_bloco_de_variaveis():
	global tokens
	if(tokens[0][2]=='variaveis\n'):
		tokens = tokens[1:]

		if(tokens[0][2]=='{\n'):
			tokens = tokens[1:]
			if(tokens[0][2]=='}\n'):
				tokens = tokens[1:]
				return True
			else:
				analisa_corpo_variavel()

			if(tokens[0][2]=='}\n'):
				tokens = tokens[1:]
				return True
			else:
				salva_erro("}")
				return False
		else:
			salva_erro("{")
			return False
	else:
		salva_erro("variaveis")
		return False

def analisa_comandos():
	global tokens
	backup = tokens

	if (analisa_comandos_aux()):
		if (analisa_comandos()):
			return True

	tokens = backup
	return True

def analisa_corpo_variavel():
	if(analisa_tipo()):
		analisa_variavel()
		analisa_prox_declaracao()

	return True

def analisa_variavel():
	global tokens
	if(tokens[0][1]=='IDE'):
		tokens = tokens[1:]
		#print(tokens[0])
		analisa_extensao_vetor()
		return True
	else:
		# salva_erro("IDE")
		return False

def analisa_prox_declaracao():
	global tokens

	if(tokens[0][2]==',\n'):
		tokens = tokens[1:]
		analisa_variavel()
		analisa_prox_declaracao()
		return True
	elif(tokens[0][2]==';\n'):
		tokens = tokens[1:]
		return analisa_corpo_variavel()
	else:
		salva_erro("; ou ,")
		return False

def analisa_extensao_vetor():
	global tokens

	if(tokens[0][2]=='[\n'):
		tokens = tokens[1:]
		#print(tokens[0])
		analisa_id_ou_num()
    
		if(tokens[0][2]==']\n'):
			tokens = tokens[1:]
			return analisa_extensao_matriz()
	return True

def analisa_extensao_matriz():
	global tokens
	if(tokens[0][2]=='[\n'):
		tokens = tokens[1:]
		analisa_id_ou_num()
		if(tokens[0][2]==']\n'):
			tokens = tokens[1:]
			
	return True

def analisa_id_ou_num():
	global tokens
	if(tokens[0][1] =='IDE' or tokens[0][1]=='NRO'):
		tokens = tokens[1:]
		return True
	else:
		salva_erro("variavel ou número")
	return False
	
def analisa_comandos_aux():
	global tokens

	if (tokens[0][1] == 'IDE'):
		if (tokens[1][2] == '=\n'):
			if(analisa_atribuicao()):
				return True
		elif(tokens[1][2] == '(\n'):
			if(analisa_chamada_de_metodo()):
				return True


	if(tokens[0][2] == 'leia\n'):
		if(analisa_leia()):
			return True
	elif(tokens[0][2] == 'escreva\n'):
		if(analisa_escreva()):
			return True
	elif(tokens[0][2] == 'enquanto\n'):
		if(analisa_lacos()):
			return True
	elif(tokens[0][2] == 'se\n'):
		if(analisa_condicionais()):
			return True

	return False

def analisa_leia():
	global tokens
	if(tokens[0][2]=='leia\n'):
		tokens = tokens[1:]
		if(tokens[0][2]=='(\n'):
			tokens = tokens[1:]
			analisa_leitura()
			analisa_leitura_aux()
			if(tokens[0][2]==')\n'):
				tokens = tokens[1:]
				if(tokens[0][2]==';\n'):
					tokens = tokens[1:]
					return True
				else:
					salva_erro(";")
					return False
			else:
				salva_erro(")")
				return False
		else:
			salva_erro("(")
			return False
	else:
		salva_erro("leia")
		return False

def analisa_leitura():
	return analisa_variavel()

def analisa_leitura_aux():
	global tokens
	backup = tokens

	if(tokens[0][2] == ',\n'):
		tokens = tokens[1:]
		return analisa_impresso() and analisa_impresso_aux()

	tokens = backup
	return True

def analisa_escreva():
	global tokens
	if(tokens[0][2] == 'escreva\n'):
		tokens = tokens[1:]
		if(tokens[0][2] == '(\n'):
			tokens = tokens[1:]
			analisa_impresso()
			analisa_impresso_aux()
			if(tokens[0][2] == ')\n'):
				tokens = tokens[1:]
				if(tokens[0][2] == ';\n'):
					tokens = tokens[1:]
					return True
				else:
					salva_erro(";")
					return False
			else:
				salva_erro(")")
				return False
		else:
			salva_erro("(")
			return False
	else:
		salva_erro("escreva")
		return False

def analisa_impresso():
	return analisa_variavel() or analisa_exp_cadeia()

def analisa_impresso_aux():
	global tokens
	backup = tokens

	if(tokens[0][2]==',\n'):
		tokens = tokens[1:]
		return (analisa_impresso() and analisa_impresso_aux())
	tokens = backup
	return True 

def analisa_exp_cadeia():
	global tokens
	if(tokens[0][1 == 'CAD']):
		tokens = tokens[1:]
		return analisa_exp_cadeia_aux()
	else:
		salva_erro("texto")
		return False

def analisa_exp_cadeia_aux():
	global tokens
	backup = tokens
	if(tokens[0][2]=='+\n'):
		tokens = tokens[1:]
		if(tokens[0][1] == 'CAD'):
			tokens = tokens[1:]
			return True

	tokens = backup
	return True

def analisa_atribuicao():
	global tokens

	if(analisa_variavel()):
		if(tokens[0][2]=='=\n'):
			tokens = tokens[1:]
			analisa_atribuiveis()
			if(tokens[0][2]==';\n'):
				tokens = tokens[1:]
				return True
			else:
				salva_erro(";")
				return False
		else:
			salva_erro("=")
			return False
	else:
		salva_erro('variavel')
		return False
def analisa_atribuiveis(): ############################################################
	global tokens
	if(tokens[0][2]=='vazio\n' or tokens[0][1]=='NRO'):
		return True
	else:
		analisa_expressoes()
		analisa_boleano()
	return True

def analisa_expressoes():
	global tokens
	if(tokens[0][1] == 'IDE'):
		if(tokens[1][1] == 'REL' ):
			return analisa_exp_relacional()
		else:
			return analisa_exp_soma() and analisa_exp_logica()
	elif(tokens[0][1] == 'REL'):
		analisa_exp_logica()

def analisa_lacos():
	global tokens

	if(tokens[0][2] == 'enquanto\n'):
		tokens = tokens[1:]
		analisa_exp_logica()
		if(tokens[0][2] == 'entao\n'):
			tokens = tokens[1:]
			if(tokens[0][2] == '{\n'):
				tokens = tokens[1:]
				analisa_corpo_metodo()
				if(tokens[0][2] == '}\n'):
					tokens = tokens[1:]

					return True
				else:
					salva_erro("}")
					return False
			else:
				salva_erro("{")
				return False
		else:
			salva_erro("entao")
			return False
	else:
		salva_erro("enquanto")
		return False

def analisa_condicionais():
	global tokens
	#print(tokens[0])
	if(tokens[0][2] == 'se\n'):
		tokens = tokens[1:]
		#print(tokens[0])
		analisa_exp_logica()
		if(tokens[0][2] == 'entao\n'):
			tokens = tokens[1:]
			if(tokens[0][2] == '{\n'):
				tokens = tokens[1:]
				analisa_corpo_metodo()
				if(tokens[0][2] == '}\n'):
					tokens = tokens[1:]
					
					analisa_condicional_else()
					return True
				else:
					salva_erro("}")
					return False
			else:
				salva_erro("{")
				return False
		else:
			salva_erro("entao")
			return False
	else:
		salva_erro("se")
		return False

def analisa_condicional_else():
	global tokens

	if(tokens[0][2] == 'senao\n'):
		tokens = tokens[1:]
		if(tokens[0][2] == '{\n'):
			tokens = tokens[1:]
			analisa_corpo_metodo()
			if(tokens[0][2]=='}\n'):
				tokens = tokens[1:]
				return True
			else:
				salva_erro("}")
				return False
		else:
			salva_erro("{")
			return False
	return True

def analisa_chamada_de_metodo():
	global tokens
	if(tokens[0][1] == 'IDE'):
		tokens = tokens[1:]
		if(tokens[0][2] == '(\n'):
			tokens = tokens[1:]
			analisa_parametro_chamada()
			if(tokens[0][2] == ')\n'):
				tokens = tokens[1:]
				if(tokens[0][2] == ';\n'):
					tokens = tokens[1:]
					return True
				else:
					salva_erro(";")
					return False
			else:
				salva_erro(")")
				return False
		else:
			salva_erro("(")
			return False
	else:
		salva_erro("nome do metodo")
		return False

def analisa_parametro_chamada():
	return analisa_variavel() and analisa_parametro_chamada_aux()

def analisa_parametro_chamada_aux():
	global tokens
	if(tokens[0][2] == ',\n'):
		tokens = tokens[1:]
		analisa_parametro_chamada()
		return True
	else:
		return True

def analisa_principal():
	global tokens
	if(tokens[0][2] == 'principal\n'):
		tokens = tokens[1:]
		if(tokens[0][2] == '{\n'):
			tokens = tokens[1:]
			analisa_corpo_metodo()
			if(tokens[0][2] == '}\n'):
				tokens = tokens[1:]
				return True
			else:
				salva_erro("}")
				return False
		else:
			salva_erro("{")
			return False
	else:
		salva_erro("principal")
		return False

def analisa_metodos():
	global tokens
	if(tokens[0][2] == 'metodo\n'):
		tokens = tokens[1:]
		if(tokens[0][1] == 'IDE'):
			tokens = tokens[1:]

			if(tokens[0][2] == '(\n'):
				tokens = tokens[1:]
				#print(tokens[0])
				analisa_parametro()
				#print(tokens[0])
				if(tokens[0][2] == ')\n'):
					tokens = tokens[1:]

					if(tokens[0][2] == ':\n'):
						tokens = tokens[1:]

						analisa_tipo_retorno()

						if(tokens[0][2] == '{\n'):
							tokens = tokens[1:]

							analisa_corpo_metodo()

							if(tokens[0][2] == '}\n'):
								tokens = tokens[1:]
								return analisa_metodos()
							else:
								salva_erro("}")
								return False
						else:
							salva_erro("{")
							return False
					else:
						salva_erro(":")
						return False
				else:
					salva_erro(")")
					return False
			else:
				salva_erro("(")
				return False
		else:
			salva_erro("nome do metodo")
			return False
	return True

def analisa_resultado_do_metodo():
	global tokens
	if(tokens[0][2]== 'vazio\n'):
		tokens = tokens[1:]
		return True
	else:
		return analisa_variavel()

def analisa_tipo_retorno():
	global tokens
	if(tokens[0][2] == 'inteiro\n' or tokens[0][2]=='real\n' or tokens[0][2]=='texto\n' or tokens[0][2]=='vazio\n' or tokens[0][2]=='boleano\n'):
		tokens = tokens[1:]
		return True
	else:
		salva_erro("inteiro, real, texto, vazio ou boleano")
		return False

def analisa_parametro():
	global tokens
	if(analisa_tipo()):
		if(tokens[0][1]=='IDE'):
			tokens = tokens[1:]
			return analisa_parametro_aux()
		else:
			salva_erro("nome do parametro")
			return False
	else:
		salva_erro("tipo do parametro")
		return False

def analisa_parametro_aux():
	global tokens
	if(tokens[0][2]==',\n'):
		tokens = tokens[1:]
		return analisa_parametro()
	else:
		return True

def analisa_operador_relacional():
	global tokens
	if(tokens[0][2] == '!=\n' or tokens[0][2] == '==\n' or tokens[0][2] ==  '<\n' or tokens[0][2] == '>\n' or tokens[0][2] ==  '<=\n' or tokens[0][2] ==  '>=\n' or tokens[0][2] ==  '=\n'):
		tokens = tokens[1:]
		return True
	else:
		salva_erro("!=, ==, <, >, <= ou >=")
		return False

def analisa_op_logico():
	global tokens
	if(tokens[0][2] == '&&\n') or (tokens[0][2] == '||\n'):
		tokens = tokens[1:]
		return True
	salva_erro("&&, ||")
	return False

def analisa_exp_soma():
	return analisa_exp_mul() and analisa_exp_art_aux()

def analisa_exp_art_aux(): #################################################
	global tokens
	if(tokens[0][2] == '++\n' or tokens[0][2] == '--\n'):
		tokens = tokens[1:]
		return True
	else:
		return (analisa_sinal1() and analisa_exp_soma()) or True

def analisa_sinal1():
	global tokens
	if(tokens[0][2] == '+\n' or tokens[0][2] == '-\n'):
		tokens = tokens[1:]
		return True
	return False

def analisa_exp_mul():
	return analisa_exp_parenteses() and analisa_exp_art_aux2()

def analisa_exp_art_aux2():
	return (analisa_sinal2() and analisa_exp_mul()) or True

def analisa_sinal2():
	global tokens
	if(tokens[0][2] == '*\n' or tokens[0][2] == '/\n'):
		tokens = tokens[1:]
		return True
	return False

def analisa_exp_parenteses():
	global tokens
	if(tokens[0][2] == '(\n'):
		tokens = tokens[1:]
		analisa_expressoes()
		if(tokens[0][2]==')\n'):
			tokens = tokens[1:]
			return True
	elif (tokens[0][1]=='NRO'):
		tokens = tokens[1:]
		return True
	else:
		return analisa_variavel()

	return False
	
def analisa_exp_relacional():
	return analisa_id_ou_num() and analisa_operador_relacional() and analisa_id_ou_num()

def analisa_exp_relacional_not():
	global tokens
	if( tokens[0][2] == '!\n' ):
		tokens = tokens[1:]
	return analisa_exp_relacional()
	return True

def analisa_boleano_aux_1():
	global tokens
	if( tokens[0][2] == '!\n' ):
		tokens = tokens[1:]
	return analisa_boleano()

def analisa_boleano_aux_2():
	global tokens
	if( tokens[0][2] == '!\n' ):
		tokens = tokens[1:]
	return analisa_variavel()

def analisa_boleano_aux():   
	return analisa_boleano_aux_1() or analisa_boleano_aux_2()

def analisa_exp_logica_aux():
	global tokens
	if (tokens[0][2] == "!\n") or (tokens[0][2] == "(\n"):
		tokens = tokens[1:]
		if (tokens[0][2] == "(\n"):
			tokens = tokens[1:]

	analisa_exp_logica_aux_2()

	if(tokens[0][2] == ")\n"):
		tokens = tokens[1:]

	return True

def analisa_exp_logica_aux_3():
	return analisa_boleano_aux() or analisa_exp_relacional_not()

def analisa_exp_logica_aux_2():
	if(analisa_exp_logica_aux_3()):
		if(analisa_op_logico()):
			if(analisa_exp_logica_aux_3()):
				return True
	return False

def analisa_exp_logica():
	global tokens

	if(analisa_exp_logica_aux()):
		analisa_exp_logica_recurrency()
		return True
	else:
		return False

def analisa_exp_logica_recurrency():
	global tokens
	backup = tokens
	if(tokens[0][2] not in('entao\n', ')\n', ';\n')):
		if(analisa_op_logico()):
			if(analisa_exp_logica()):
				return True

	tokens = backup

	return True

def salva_erro(esperado):
	global erros
	global tokens
	global output

	erros = tokens[0]

	print('ERRO '+esperado)
	print(erros)
	
	linha = erros[0]
	token = erros[1]
	valor = erros[2]
	valor = valor[:-1] #remove o \n

	#LOGICA DE SALVAR O ERRO NO ARQUIVO
	output.write("Linha do erro: "+linha+". Recebeu \""+valor+", "+token+"\", mas esperava \""+esperado+"\".\n")
	

	# sys.exit("ERRO! (verificar arquivo de erros)") #finaliza o programa
