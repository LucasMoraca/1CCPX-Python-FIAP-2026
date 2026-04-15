num_1 = float(input("Digite o primeiro número: "))
num_2 = float(input("Digite o segundo número: "))
opracoes = input("Digite a operação (+, -, *, /): ")

if opracoes == "+":
  print(num_1 + num_2)
elif opracoes == "-":
  print(num_1 - num_2)
elif opracoes == "*":
  print(num_1 * num_2)
elif opracoes == "/":
  print(num_1 / num_2)
else:
  print("Operação inválida")
