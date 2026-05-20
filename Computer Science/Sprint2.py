# 1. Definição das Entradas (Variáveis Simuladas)
# Altere os valores lógicos (1 para Verdadeiro, 0 para Falso) para testar os cenários.

A = 1  # Confirmação de Pagamento: 1 para aprovado, 0 para não encontrado
B = 1  # Autenticação RFID: 1 para autenticado, 0 para negado
C = 1  # Engate do Cabo: 1 para conectado, 0 para desconectado
M = 0  # Manutenção: 1 para liberação técnica, 0 para operação padrão

# 2. Expressão Booleana e Lógica do Sistema
# S = (A and B and C) or M
# A variável S atua como orquestrador da entrega de energia.

S = (A == 1 and B == 1 and C == 1) or (M == 1)

# 3. Condicionais e Impressão de Resultados
print("--- Status do Eletroposto ---")

if M == 1:
    # Cenário de Gestão Remota (Porta OR)
    print("Status: Manutenção - Bypass remoto ativo.")
    print("Saída S = 1 (Liberação de corrente elétrica e travamento do cabo autorizados)")
    
elif S == True:
    # Cenário de Operação Normal (Porta AND)
    print("Status: Sucesso - Operação Comercial Ativa.")
    print("Saída S = 1 (Liberação de corrente elétrica e travamento do cabo autorizados)")
    
else:
    # Cenário de Falha em um dos pilares comerciais ou de segurança física
    print("Status: Bloqueado.")
    print("Saída S = 0 (Interrupção do fluxo de energia e desbloqueio do cabo)")
    
    # Detalhamento das falhas locais
    if A == 0:
        print(" -> Alerta: Falha no faturamento/pagamento não encontrado.")
    if B == 0:
        print(" -> Alerta: Usuário sem autenticação RFID.")
    if C == 0:
        print(" -> Alerta: Cabo desconectado fisicamente.")