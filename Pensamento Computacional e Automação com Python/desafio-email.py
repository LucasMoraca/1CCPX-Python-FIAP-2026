entrada = input("Digite os e-mails separados por vírgula: ")

# Separa os e-mails e remove espaços extras
emails = entrada.split(",")

usuarios = []
dominios = {}

for email in emails:
    email = email.strip()

    # Separa usuário e domínio
    usuario, dominio = email.split("@")

    usuarios.append(usuario)

    # Conta a quantidade de e-mails por domínio
    if dominio not in dominios:
        dominios[dominio] = 1
    else:
        dominios[dominio] += 1

# Converte a lista de usuários em uma tupla
usuarios = tuple(usuarios)

print("\nRelatório:")
print("Quantidade de e-mails por domínio:")

for dominio, quantidade in dominios.items():
    print(f"{dominio}: {quantidade}")

print(f"\nLista de usuários: {usuarios}")

# Exibe o primeiro e o último usuário
print(f"Primeiro usuário: {usuarios[0]}")
print(f"Último usuário: {usuarios[-1]}")

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