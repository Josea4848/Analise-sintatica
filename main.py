class Token:
  def __init__(self, token, tipo, linha) -> None:
    self.token = token
    self.tipo = tipo
    self.linha = linha

class Sintatico:
  def __init__(self, listTokens):
    self.tokens = listTokens
    self.posicao = 0
    self.erros = list()
    self.token = tokens[0]

  #Avança token
  def next(self):
    if(self.posicao + 1 < len(self.tokens)):
      self.posicao += 1
      self.token = tokens[self.posicao]

  #program inicia e terminará a análise
  def program(self):
    if self.token.token == "program":
      self.next()  
      if self.token.tipo == "id":
        self.next()
        if self.token.token == ";":
          self.next()
          self.declaracao_variaveis()
          self.declaracao_de_subprogramas()
          self.comando_composto()

          if self.token.token != ".":
            self.erros.append(". expected at the end of the program")
        else:
          self.erros.append(f"[{self.token.linha}] ; missing")
      else:
        self.erros.append(f"[{self.token.linha}] ID inválido")
    else:
      self.erros.append(f"[{self.token.linha}] Inicializador program não encontrado")     

  #bloco de declaração de variáveis
  def declaracao_variaveis(self):
    if(self.token.token == "var"): #esse if impede e volta pra program
      self.next()
      self.lista_declaracao_variaveis()
    #token ->  ε
    else:
      pass
    
  def lista_declaracao_variaveis(self):
    self.lista_indentificadores()
    if self.token.token == ":":
      self.next()
      self.tipo()
      
      if self.token.token != ";":
        self.erros.append(f"; missing, line {self.tokens[self.posicao - 1].linha}")
      else:
        self.next()

      if self.token.tipo == "id":
        self.lista_declaracao_variaveis()
    else:
      self.erros.append(f"[{self.token.linha}] : expected")
    
  def lista_indentificadores(self):
    if self.token.tipo == "id":
      self.next()
      self.lista_indentificadores2()

    else:
      self.erros.append(f"[{self.token.linha}] id inválido {self.token.token}")

  def lista_indentificadores2(self): #,id(ldi')/ ε
    if self.token.token == ",":
      self.next()
      #se espera um id
      if(self.token.tipo == "id"):
        self.next()
        self.lista_indentificadores2()
      else:
        self.erros.append(f"ID inválido {self.token.token}")

    else:
      pass
  
  def tipo(self):
    if(self.token.token in ['real','integer','boolean']):
      self.next()
    else:
      self.erros.append(f"{self.token.token}: Tipo inválido")
      self.next()

  def declaracao_de_subprogramas(self): #D_SUBPROGMS
    
    if self.token.token == "procedure":
      self.next()
      self.declaracao_de_subprograma()
      self.declaracao_de_subprogramas2()
    else:
      pass
  
  def declaracao_de_subprogramas2(self): #D_SUBPROGMS'
    if(self.token.token == "procedure"):
      self.next()
      self.declaracao_de_subprograma()
      self.declaracao_de_subprogramas2()
    else:
      pass

  def declaracao_de_subprograma(self): #d_subprgm
    if self.token.tipo == "id":
      self.next()
      self.argumentos()
      if self.token.token == ";":
        self.next()
      else:
        self.erros.append(f"; missing, line {self.tokens[self.posicao - 1].linha}")

      self.declaracao_variaveis()
      self.declaracao_de_subprogramas()

    else:
      self.erros.append(f"ID inválido {self.token.token}")

  def argumentos(self):
    if self.token.token == "(":
      self.next()
      self.lista_de_parametros()

      if self.token.token == ")":
        self.next()
      else:
        self.erros.append(") expected")

    else:
      pass

  def lista_de_parametros(self):
    self.lista_indentificadores()
    if(self.token.token == ":" or self.token.token == ";"):
      if self.token.token == ";":
          self.erros.append("; is not :")
      self.next()  
    else:
      self.erros.append(": expected")
    
    self.tipo()
    self.lista_de_parametros2()

  
  def lista_de_parametros2(self):
    if self.token.token == ";":
      self.next()
      self.lista_indentificadores()

      if(self.token.token == ":"):
        self.next()
        
      else:
        self.erros.append(": expected")  

      self.tipo()

      self.lista_indentificadores2()

    else:
      pass

  def comando_composto(self):
    if self.token.token == "begin":
      self.next()
      self.comandos_opcionais()
      
      if self.token.token == "end":
        self.next()
      else:
        self.erros.append(f"Expected end, line {self.token.linha}")
    else:
      self.erros.append("begin expected")

  def comandos_opcionais(self):
    self.lista_de_comandos()
  
  def lista_de_comandos(self):
    self.comando()
    self.lista_de_comandos2()


  def lista_de_comandos2(self):
    if self.token.token in ['(','if','while','begin'] or self.token.tipo == "id":
      self.comando()
      self.lista_de_comandos2()

  def comando(self):
    #se lê ID
    if self.token.tipo == "id":
      self.next()

      if self.token.token == ":=":
        self.next() 
        self.expressao()
        if self.token.token == ";":
          self.next()
        else:
          self.erros.append(f"; missing, line {self.tokens[self.posicao - 1].linha}")
      
      if self.token.token == "(":
        self.next()
        self.ativacao_de_procedimento()

    elif self.token.token == "if":
      self.next()
      if self.token.token == "(":
        self.next()
        self.expressao()
        if self.token.token == ")":
          self.next()
        else:
          self.erros.append(f") expected {self.tokens[self.posicao - 1].linha}")
      else:
        self.expressao()

        if self.token.token == ")":
          self.erros.append(f"( expected, line {self.token.linha}")
          self.next()

      if self.token.token == "then":
        self.next()
      else:
        self.erros.append("expected [then keyword]")

      #comando dentro de comando      
      if self.token.token == "begin":
        self.comando_composto()
      else:
        self.comandos_opcionais()

      self.parte_else()

    elif self.token.token == "while":
      self.next()
      #while()
      if self.token.token == "(":
        self.next()
        self.expressao()
        if self.token.token == ")":
          self.next()
        else:
          self.erros.append(f") expected, line {self.tokens[self.tokens.posicao-1].linha}")
      else:
        self.expressao()
        if self.token.token == ")":
          self.erros.append(f"( expected, line {self.token.linha}")
          self.next()

      if self.token.token == "do":
        self.next()
      else:
        self.erros.append("Expected 'do' keyword")
      
      if self.token.token == "begin":
        self.comando_composto()
      else:
        self.comandos_opcionais

      #recursão novamente
      self.comando()
    
    elif self.token.token == "begin":
      self.comandos_opcionais()

    else:
      pass


  def ativacao_de_procedimento(self):
    self.lista_de_expressoes()
    if self.token.token == ")":
      self.next()
    else:
      self.erros.append(f") expected, {self.token.linha}")
  

  def lista_de_expressoes(self):
    self.expressao()
    self.lista_de_expressoes2()

  def lista_de_expressoes2(self):
    if self.token.token == ",":
      self.next()
      self.expressao()
      self.lista_de_expressoes2()

  def expressao(self):
    self.expressao_simples()

    if self.token.token in ["=", "<", ">", "<=", ">=", "<>"]:
      self.next()
      self.expressao_simples()

  def expressao_simples(self):
    self.termo()
    self.expressao_simples2()

  def expressao_simples2(self):
    if self.token.token in ["+", "-"]:
      self.next()
      self.termo()
      self.expressao_simples2()
    else:
      pass

  def termo(self):
    self.fator()
    self.termo2()

  def termo2(self):
    if self.token.token in "*/":
      self.next()
      self.fator()
      self.termo2()

  def fator(self):
    #(expressão)
    if self.token.token == "(":  
      self.next()
      self.expressao()

      if self.token.token == ")":
        self.next()
      else:
        self.erros.append(f") expected, line {self.token.linha}")
    
    #real, inteiro, true ou false
    elif self.token.tipo in ["real", "integer", "bool"]:
      self.next()      
    
    #id
    elif self.token.tipo == "id":
      self.next()
      #id(expressão)
      if self.token.token == "(":
        self.lista_de_expressoes()
        if self.token.token == ")":
          self.next()
        else:
          self.erros.append(") expected")

    #not fator
    elif self.token.token == "not":
      self.next()
      self.fator()

    else:
      self.erros.append("Valor inválido")
      self.next()

  def parte_else(self):
    if self.token.token == "else":
      self.next()
      self.comando()
    #token ->  ε
    else:
      pass

    
#Leitura dos tokens -> token | tipo
tokensFile = open("tabela2.csv", "r")
lines = tokensFile.readlines()
lines.pop(0)

#array de tokens
tokens = list()

#Adiciona tokens ao dicionário
for line in lines:
  line = line.split(" ")
  tokens.append(Token(line[0], line[1], line[2].replace("\n","")))


app = Sintatico(tokens)
app.program()

#verifica erro
for erro in app.erros:
  print(f'\033[31m"{erro}"\033[m')

app.fator()