# Exercício 1
resposta = "s"

while resposta == "s":
    print("Olá, Mundo")
    resposta = input("Deseja exibir novamente? (s/n): ").lower()  # O .lower() permite que o Sim seja diferente do s, que seria o padrão

print("Fim")

# Exercício 2
# range(inicio, fim, incremento)
# "conte de X até Y pulando de Z em Z"
# for variavel in range(X, Y + 1, Z):

for numero in range(0, 101, 10):
    print(numero)

# Exercício 3
# Validação da entrada
n = int(input('Digite um número positivo: '))

while n <= 0:
    print('Valor inválido! Digite apenas números positivos.')
    n = int(input('Difite um número positivo: '))

# Soma dos números
soma = 0

for numero in range(1, n + 1):
    soma += numero

# Resultado
print(f'A soma de 1 até {n} é: {soma}')

# Exercício 4
n = int(input("Digite um número positivo: "))

print(f"Divisores de {n}:")

for numero in range(1, n + 1):  # for numero in range(1, n + 1):
    if n % numero == 0:         # if n % numero == 0:
        print(numero)

# Exercício 5
print('\nExercício 5')
for numero in range(2, 2001):  # Percorre cada número entre 2 e 2000

    quantidade_divisores = 0

    for divisor in range(1, numero + 1): # Para cada número, verificamos seus divisores

        if numero % divisor == 0:
            quantidade_divisores += 1

    if quantidade_divisores == 2:
        print(numero)

# Exercício 6
import random

n = int(input("Digite a quantidade de números: "))

vetor = []  # lista vazia

for i in range(n):  # Execute n vezes
    numero = random.uniform(0, 100)
    vetor.append(numero)

print("\nNúmeros gerados:")

for numero in vetor:
    print(numero)

# Exercício 7
n = int(input("Digite o tamanho do vetor: "))

vetor = []

for i in range(n):
    caractere = input(f"Digite o caractere da posição {i}: ")
    vetor.append(caractere)

print("\nVetor original:")
print(vetor)

for i in range(n // 2):
    vetor[i], vetor[n - 1 - i] = vetor[n - 1 - i], vetor[i]

print("\nVetor invertido:")
print(vetor)

# Exercício 8
linhas = int(input("Digite a quantidade de linhas: "))
colunas = int(input("Digite a quantidade de colunas: "))

A = []
B = []

print("\nPreenchendo a matriz A")

for i in range(linhas):
    linha = []

    for j in range(colunas):
        valor = int(input(f"A[{i}][{j}]: "))
        linha.append(valor)

    A.append(linha)

print("\nPreenchendo a matriz B")

for i in range(linhas):
    linha = []

    for j in range(colunas):
        valor = int(input(f"B[{i}][{j}]: "))
        linha.append(valor)

    B.append(linha)

C = []

for i in range(linhas):

    linha = []

    for j in range(colunas):
        linha.append(A[i][j] + B[i][j])

    C.append(linha)

print("\nMatriz resultado:")

for linha in C:
    print(linha)
