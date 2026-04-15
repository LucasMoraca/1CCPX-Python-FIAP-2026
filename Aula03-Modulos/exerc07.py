nasc = int(input("Digite o ano de nascimento: "))
idade = 2026 - nasc

if idade >= 18 and idade < 70:
  print("Voto obrigatório este ano")
elif idade >= 16 and idade < 18 or idade >= 70:
  print("Voto opcional este ano")
else:
  print("Voto proibido este ano")
