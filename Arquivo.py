# -*- coding: utf-8 -*-
class Arquivo:
	caminho = ''
	
	def __init__(self, caminho):
		self.caminho = caminho

	def caracteres():
		with open(caminho) as arq:
			linhas = arq.readlines()
			for linha in linhas:
				for caractere in linha:
					carac.append(caractere)
		return carac