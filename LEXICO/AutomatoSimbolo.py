# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 2019

@author: Antonio Raian e Diogo Lima
"""
ARITMETICOS = ['+', '-', '*', '/', '++', '--']
SIMBOLOS = ['@','#', '$', '%', '&', '?', '|']  #'&&', '||'

def automato_simbolo(palavra):
    if(len(palavra)>2):
        return ('1',"ERR_SIM " + palavra)
    if(len(palavra)==2):
        if(palavra[0]=='&' and palavra[len(palavra)-1] == '&'):
            return ('2',"LOG " + palavra)
        if(palavra[0]=='|' and palavra[len(palavra)-1] == '|'):
            return ('2',"LOG " + palavra)
    #     if(palavra[0]=='+' and palavra[len(palavra)-1] == '+'):
    #         return ('2',"ARI " + palavra)
    #     if(palavra[0]=='-' and palavra[len(palavra)-1] == '-'):
    #         return ('2',"ARI " + palavra)
    # else:    
    #     return ('2',"ARI " + palavra)
    
    return ('1',"ERR_SIM " + palavra)