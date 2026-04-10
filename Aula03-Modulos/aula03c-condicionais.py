# Operadores de atribuição
from operator import truediv

num = 15
print(num)

num = num + 2
print(num) #17

num *= 2
print(num)

# Operadores relacionais
print() # pular linha
print(6 == 3)
print(6 != 3)
print(6 > 3)
print(6 <= 3)

print()

idade = 20
print(idade == 20)

maior_idade = idade >= 18
print(maior_idade)

# Operadores Lógicos
# Lógica e (and)
print()

verifica_email = True
verifica_senha = False

login = verifica_email and verifica_senha
print(login)

if login:
    print("Entrar no programa")
if not login:
    print("Po cara acerta ai...")

print()
# Notas

nota_final = 6

if nota_final < 4:
    print("Reprovado")
elif nota_final < 6:
    print("Recuperação")
else:
    print("Aprovado")

print("FIM")