# Entrada de dados
estado = int(input("Digite o código do estado (1 a 5): "))
toneladas = float(input("Digite o peso da carga em toneladas: "))
codigo = int(input("Digite o código da carga (10 a 40): "))

# Conversão de toneladas para quilos
kg = toneladas * 1000

# Preço por kg de acordo com o código da carga
if 10 <= codigo <= 20:
    preco_por_kg = 100
elif 21 <= codigo <= 30:
    preco_por_kg = 250
elif 31 <= codigo <= 40:
    preco_por_kg = 340

# Preço da carga
preco_carga = kg * preco_por_kg

# Cálculo do imposto conforme o estado
if estado == 1:
    imposto = preco_carga * 0.35
elif estado == 2:
    imposto = preco_carga * 0.25
elif estado == 3:
    imposto = preco_carga * 0.15
elif estado == 4:
    imposto = preco_carga * 0.05
else:  # estado == 5
    imposto = 0

# Valor total
valor_total = preco_carga + imposto

# Saída
print("\n--- DADOS DA CARGA ---")
print(f"Peso da carga em kg: {kg:.2f}")
print(f"Preço da carga: R$ {preco_carga:.2f}")
print(f"Valor do imposto: R$ {imposto:.2f}")
print(f"Valor total transportado: R$ {valor_total:.2f}")