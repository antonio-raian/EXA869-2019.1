#CÃ³digo principal do compilador
# -*- coding: utf-8 -*-

from LEXICO import main as lexico
from SINTATICO import main as sintatico
from Semantico import main as semantico

lexico.main()
sintatico.main()
semantico.main()