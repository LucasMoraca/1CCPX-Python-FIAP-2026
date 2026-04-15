num_1 = int(input("Digite o primeiro número: "))
num_2 = int(input("Digite o segundo número: "))

if num_1 % num_2 == 0 or num_2 % num_1 == 0:
  print("São múltiplos")
else:
  print("Não são múltiplos")
