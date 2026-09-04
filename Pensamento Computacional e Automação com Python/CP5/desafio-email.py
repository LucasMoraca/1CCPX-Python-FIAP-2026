# DESAFIO: ANALISADOR DE E-MAILS DA FIAP

# Entrada dos dados
entrada = input('Digite os e-mails separados por vírgula: ')

# Separação dos e-mails
emails = entrada.split(',')

# Criação das estruturas
usuarios = [] # Lista vazia
dominios = {} # Dicionário vazio

for email in emails: # o for percorre cada item da lista emails
    email = email.strip() # o método strip() remove os espaços no início e no final do texto

    # Usando o método split('@') vamos dividir o e-mail em duas partes, sendo uma usuário e outra em domínio
    usuario, dominio = email.split('@')

    usuarios.append(usuario) # Adiciona o usuário na lista usuarios

    # Conta a quantidade de e-mails por domínio
    if dominio not in dominios:  # Verifica se o domínio já existe no dicionário.
        dominios[dominio] = 1  # Caso o domínio ainda não exista Cria a chave e inicia a contagem em 1.
    else:
        dominios[dominio] += 1  # Caso já exista Incrementa a quantidade.

# Converte a lista de usuários em uma tupla
usuarios = tuple(usuarios)


# Cabeçalho
print('\nRelatório')
print('Quantidade de e-mails por domínio: ')

# Percorre o dicionário
for dominio, quantidade in dominios.items():  # O método items() devolve pares
    print(f"{dominio}: {quantidade}")

print(f"\nLista de usuários: {usuarios}")

# Exibe o primeiro e o último usuário
print(f'Primeiro usuário: {usuarios[0]}')
print(f'Último usuário: {usuarios[-1]}')

# Como tuplas são imutáveis, criamos uma lista temporária
usuarios_trocados = list(usuarios)

# Troca sem variável temporária
usuarios_trocados[0], usuarios_trocados[-1] = (
    usuarios_trocados[-1],
    usuarios_trocados[0]
)

# Converte novamente para tupla
usuarios_trocados = tuple(usuarios_trocados)

print(f"Após troca de posições: {usuarios_trocados}")
