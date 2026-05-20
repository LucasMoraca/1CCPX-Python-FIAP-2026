# 1. Definição das Entradas (Variáveis Simuladas)
# Altere os valores (1 ou 0) para testar a tabela verdade do sistema.

A = 1  # Confirmação de Pagamento: 1 (Aprovado), 0 (Não encontrado)
B = 1  # Autenticação RFID: 1 (Autenticado), 0 (Acesso negado)
C = 1  # Engate do Cabo: 1 (Conectado), 0 (Desconectado)
M = 0  # Manutenção: 1 (Bypass remoto ativo), 0 (Operação normal)

# Expressão Booleana: S = (A and B and C) or M
# Utiliza-se 'and' explícito para a conjunção comercial e 'or' para a disjunção de gestão remota.

S = (A == 1 and B == 1 and C == 1) or (M == 1)

# 3. Condicionais e Impressão de Resultados
print("--- Status do Eletroposto ChargeGrid ---")

if S == True:
    if M == 1:
        # Bloco de Disjunção (Porta OR) forçou a ativação
        print("Status: Manutenção - Bypass remoto ativo.")
        print("Saída S = 1 (Liberação do sistema para intervenção técnica/destravamento)")
    else:
        # Bloco de Conjunção (Porta AND) foi totalmente validado
        print("Status: Sucesso - Operação Comercial Ativa.")
        print("Saída S = 1 (Pagamento, RFID e Cabo validados. Energia liberada)")
        
else:
    # Saída bloqueada pela Porta AND durante a operação normal (M=0)
    print("Status: Bloqueado.")
    print("Saída S = 0 (Interrupção do fluxo de energia e desbloqueio do cabo)")
    
    # Validação individual das variáveis para identificar a falha
    if A == 0:
        print(" -> Alerta: Falha no faturamento/pagamento não encontrado.")
    if B == 0:
        print(" -> Alerta: Usuário sem autenticação RFID.")
    if C == 0:
        print(" -> Alerta: Cabo desconectado fisicamente.")