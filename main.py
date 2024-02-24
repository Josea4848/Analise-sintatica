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

          #if self.token.token != ".":
            #self.erro = True
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
        self.erros.append(f"; missing")
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
        self.erros.append("ID inválido")

    else:
      pass
  
  def tipo(self):
    if(self.token.token in ['real','integer','boolean']):
      self.next()
    else:
      self.erros.append("Tipo inválido")
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
        self.erros.append("; missing")

      self.declaracao_variaveis()
      self.declaracao_de_subprograma()

    else:
      self.erros.append("ID inválido")

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
      pass
    else:
      self.erros.append("begin expected")

  def comandos_opcionais(self):
    pass
  
  def lista_de_comandos(self):
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
print(app.erros)
