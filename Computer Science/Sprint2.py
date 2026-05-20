# 1. Definição das Entradas (Variáveis Simuladas)
# Altere os valores para testar diferentes cenários.

A = 1  # Confirmação de Pagamento: 1 para aprovado, 0 para não encontrado
B = 1  # Autenticação RFID: 1 para autenticado, 0 para negado
C = 1  # Engate do Cabo: 1 para conectado, 0 para desconectado
M = 0  # Manutenção: 1 para manutenção ativa, 0 para operação normal

# 2. Lógica do Sistema Corrigida
# A energia (S) SÓ é liberada se os 3 pilares comerciais estiverem validados (A, B, C)
# E se o sistema NÃO estiver em manutenção (M == 0).
S = (A == 1 and B == 1 and C == 1) and (M == 0)

# 3. Condicionais e Impressão de Resultados
print("--- Status do Eletroposto ChargeGrid ---")

if M == 1:
    # Cenário de Manutenção (Bloqueio Absoluto)
    print("Status: Em Manutenção.")
    print("Saída S = 0 (Fluxo de energia bloqueado por segurança para intervenção técnica)")
    
elif S == True:
    # Cenário de Operação Normal (Todos os requisitos validados)
    print("Status: Sucesso - Operação Comercial Ativa.")
    print("Saída S = 1 (Liberação de corrente elétrica e travamento do cabo autorizados)")
    
else:
    # Cenário de Falha Operacional
    print("Status: Bloqueado.")
    print("Saída S = 0 (Interrupção do fluxo de energia e desbloqueio do cabo)")
    
    # Detalhamento de qual pilar falhou
    if A == 0:
        print(" -> Alerta: Falha no faturamento/pagamento não encontrado.")
    if B == 0:
        print(" -> Alerta: Usuário sem autenticação RFID.")
    if C == 0:
        print(" -> Alerta: Cabo desconectado fisicamente.")