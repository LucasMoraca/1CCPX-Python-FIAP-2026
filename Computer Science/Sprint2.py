# 1. Definição das Entradas (Variáveis Simuladas)
# Altere os valores (1 ou 0) para testar a tabela verdade do sistema.

A = 1  # Confirmação de Pagamento: 1 (Aprovado), 0 (Não encontrado)
B = 1  # Autenticação RFID: 1 (Autenticado), 0 (Acesso negado)
C = 1  # Engate do Cabo: 1 (Conectado), 0 (Desconectado)
M = 0  # Manutenção: 1 (Bypass remoto ativo), 0 (Operação normal)

# 2. Lógica do Sistema
# A operação comercial depende da conjunção simultânea de A, B e C.
# A manutenção (M) atua no bloco de disjunção, sobrepondo o bloqueio local.
# Em Python, valores 1 e 0 são avaliados nativamente como True e False.

S = (A and B and C) or M

# 3. Condicionais e Impressão de Resultados
print("--- Status do Eletroposto ChargeGrid ---")

if S:
    if M:
        # A manutenção sobrepõe as variáveis comerciais, forçando a saída ativa
        print("Status: Manutenção - Bypass remoto ativo.")
        print("Saída S = 1 (Liberação do sistema para intervenção técnica/destravamento)")
    else:
        # O bloco de conjunção foi 100% validado na operação normal
        print("Status: Sucesso - Operação Comercial Ativa.")
        print("Saída S = 1 (Pagamento, RFID e Cabo validados. Energia liberada)")
        
else:
    # A energia é cortada se faltar qualquer um dos três sinais comerciais
    print("Status: Bloqueado.")
    print("Saída S = 0 (Interrupção do fluxo de energia e desbloqueio do cabo)")
    
    # Validação individual das variáveis lógicas para identificar a falha
    if not A:
        print(" -> Alerta: Falha no faturamento/pagamento não encontrado.")
    if not B:
        print(" -> Alerta: Usuário sem autenticação RFID.")
    if not C:
        print(" -> Alerta: Cabo desconectado fisicamente.")