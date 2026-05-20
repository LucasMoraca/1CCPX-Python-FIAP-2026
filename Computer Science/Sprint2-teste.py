# Algoritmo em Python que representa o circuito lógico da Sprint 1

# Definição das entradas do sistema
# A = pagamento aprovado
# B = autenticação RFID
# C = cabo conectado
# M = manutenção ativada

A = int(input("Pagamento aprovado? (0 ou 1): "))
B = int(input("Autenticação RFID? (0 ou 1): "))
C = int(input("Cabo conectado? (0 ou 1): "))
M = int(input("Manutenção ativada? (0 ou 1): "))

# Lógica do circuito
# Se estiver em manutenção, a saída é liberada.
# Caso contrário, a saída só é liberada se A, B e C forem 1 ao mesmo tempo.
if M == 1 or (A == 1 and B == 1 and C == 1):
    print("Potência liberada")
else:
    print("Potência bloqueada")