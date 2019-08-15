tokens = ""

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

			if analisa_corpo_code():

				esperado = "}\n"

				if tokens[1][2] == esperado
					tokens = tokens[1:]


def analisa_corpo_code():
	global tokens
	backup = tokens

	if analisa_constantes():
		if analisa_bloco_de_metodos():
			if analisa_principal():
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

			if analisa_corpo_constantes():

				esperado = "}\n"

				if tokens[1][2] == esperado
					tokens = tokens[1:]

					return true


def analisa_corpo_constantes():		#ACEITA VAZIO. PORTANTO, DEVE PODER RETORNAR AO BACKUP CASO ENCONTRE ERRO.		
	global tokens
	backup = tokens

	if analisa_tipo():
		esperado = "IDE"

		if tokens[1][1] == esperado:
			tokens = tokens[1:]

			esperado = "=\n"
			if tokens[1][2] == esperado:
				tokens = tokens[1:]

				if analisa_valor_atribuido():

					if analisa_prox_declaracao_constantes():

						return true
	#SE ALGUMA DAS CONDICOES NAO FOR VERDADEIRA

	tokens = backup
	return true						

def analisa_prox_declaracao_constantes():
	global tokens
	backup = tokens

	#TODO



def analisa_tipo():
	global tokens
	backup = tokens

	if tokens[1][2] == "inteiro\n" || "real\n" || "texto\n" || "boleano\n":
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
	elif tokens[1][1] == "CAD" | "NRO":
		tokens = tokens[1:]

		return true
	else:
		return false	


def analisa_boleano():
	global tokens
	backup = tokens

	if tokens[1][2] == "verdadeiro\n" || "falso\n":
		tokens = tokens[1:]

		return true
	else:
		return false
