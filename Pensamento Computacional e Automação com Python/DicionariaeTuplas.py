# Exemplo de construção de um dicionário
# Aqui no exemplo vamos construiri um dicionário do inglês para o espanhol

eng2sp = dict() # Aqui mostramos que o dicionário está vazio
print(eng2sp)

eng2sp['one'] = 'uno' # cadastro de itens no dicionário
print(eng2sp)

# O operador in informa se o termo é uma chave do dicionário ou se ele é um termo relacionado, se ele for a chave será True
print('one' in eng2sp) 
print('uno' in eng2sp)

# Usamos o vals para verificar se o termo está cadastrado como um valor, se for um valor será True
vals = eng2sp.values()
print('uno' in vals)
print('one' in vals)

# Estudo de caso:
# Vamos construir um contador de caracteres com dicionário

texto = input('Informe a palavra desejada: ')

contadores = {}  # Criando o dicionário vazio

for caractere in texto:  # Percorre cada caractere da string
    if caractere not in contadores:
        contadores[caractere] = 1  # Se o caractere ainda não existe no dicionário, adiciona com valor 1
    else:
        contadores[caractere] += 1  # Se já existe, incrementa o valor

print(contadores)

# Outro modo de fazer

contadores = {}

for caractere in texto:
    contadores[caractere] = contadores.get(caractere, 0) + 1 # o .get() procura uma chave dentro do dicionário -> dicionario.get(chave, valor_padrao)

print(contadores)

# Estudando Tuplas
# Sintaticamente, uma tupla é uma lista de valores separados por vírgulas

frutas = ('maçã', 'banana', 'laranja')

print(frutas)

print(frutas[2])  # Seguem a mesma ideia de índice das listas, começando no 0

# Percorrendo uma tupla com for
for fruta in frutas:
    print(fruta)

# Descobrindo o tamanho de uma tupla
print(len(frutas))

# Exemplo prático
# Tuplas são muito utilizadas para armazenar informações que não devem alterar
funcionario = (
    'Lucas',
    'Estagiário',
    'Palmeiras'
)

# Desempacotamento de tupla
nome, cargo, time = funcionario

print('Nome: ', nome)
print('Cargo: ', cargo)
print('Time: ', time)

print('Nome: ', funcionario[0])
print('Time: ', funcionario[2])
print('Cargo: ', funcionario[1])

# Tuplas são imutáveis
