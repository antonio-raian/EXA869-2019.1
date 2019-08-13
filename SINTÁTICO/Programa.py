def main(tokens):
    print(tokens)
    for token in tokens:
        n_linha = token[0]
        tipo = token[1]
        value = token[2]
        print('LINHA '+n_linha+ '->TIPO '+tipo+'->VALOR '+value)