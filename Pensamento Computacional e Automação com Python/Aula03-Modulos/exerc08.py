salario = float(input("Informe o seu salário: "))

if salario <= 280:
  percentual = 0.2
elif salario <= 700:
  percentual = 0.15
elif salario <= 1500:
  percentual = 0.1
else:
  percentual = 0.0

valor_aumento = salario * percentual
novo_salario = salario + valor_aumento

print("\n--- Reajuste Salarial ---")
print(f"Salário antes do reajuste: R$ {salario:.2f}")
print(f"Percentual de aumento aplicado: {percentual * 100:.0f}%")
print(f"Valor do aumento: R$ {valor_aumento:.2f}")
print(f"Novo salário após o reajuste: R$ {novo_salario:.2f}")
