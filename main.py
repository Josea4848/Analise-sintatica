#tokens
tokens = {"token":[], "tipo":[]}

#Leitura dos tokens -> token | tipo
tokensFile = open("tabela2.csv", "r")
lines = tokensFile.readlines()
lines.pop(0)

#Adiciona tokens ao dicionário
for line in lines:
  line = line.replace('"',"").split(";")
  tokens["token"].append(line[0])
  tokens["tipo"].append(line[1])

for k,c  in tokens.items():
  print(f"{k} {c}")