class Token:
  def __init__(self, token, tipo) -> None:
    self.token = token
    self.tipo = tipo

class Sintatico:
  def __init__(self, listTokens):
    self.tokens = listTokens
    self.posicao = 0
    self.erro = False
    self.token = tokens[0]

  def next(self):
    self.posicao += 1
    self.token = tokens[self.posicao]

  def program(self):
    if self.token.token == "program":
      self.next()  
      if self.token.tipo == "id":
        self.next()
        if self.token.token == ";":
          print("program id;")
        else:
          self.erro = True     
      else:
        self.erro = True      
    else:
      self.erro = True     



#Leitura dos tokens -> token | tipo
tokensFile = open("tabela2.csv", "r")
lines = tokensFile.readlines()
lines.pop(0)

#array de tokens
tokens = list()

#Adiciona tokens ao dicionário
for line in lines:
  line = line.split(" ")
  tokens.append(Token(line[0], line[1]))


for token in tokens:
  print(f"{token.token} {token.tipo}")



app = Sintatico(tokens)
app.program()