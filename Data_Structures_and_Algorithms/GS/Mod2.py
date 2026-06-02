import datetime
import random

# Lista global para armazenar as leituras
historico = []

def simular_dados():
    """
    Simula a recepção de dados automáticos vindo dos sensores da nave.
    Gera valores aleatórios coerentes para testes rápidos do sistema.
    """
    print("\n--- Simular Dados dos Sensores ---")
    
    # Simulação realista de dados
    temperatura = round(random.uniform(50.0, 100.0), 1)
    energia = round(random.uniform(10.0, 100.0), 1)
    comunicacao = random.choice([0, 1])
    
    leitura = {
        'temperatura': temperatura,
        'energia': energia,
        'comunicacao': comunicacao,
        'data_hora': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Define o status operacional do dado simulado e salva no histórico
    leitura['status_operacional'] = status_operacional(leitura)
    historico.append(leitura)
    
    print("Telemetria simulada capturada com sucesso!")
    print(f" -> Temperatura: {temperatura}°C")
    print(f" -> Energia: {energia}%")
    print(f" -> Comunicação: {'Ok' if comunicacao == 1 else 'Falha'}")
    print(f" -> Status Derivado: {leitura['status_operacional']}")

def inserir_dados():
    """Recebe manualmente os dados dos sensores e os armazena no histórico."""
    print("\n--- Inserir Novos Dados Manualmente ---")
    try:
        temperatura = float(input("Digite a temperatura (°C): "))
        energia = float(input("Digite o nível de energia (%): "))
        comunicacao = int(input("Digite o status da comunicação (1 = Ok, 0 = Falha): "))

        leitura = {
            'temperatura': temperatura,
            'energia': energia,
            'comunicacao': comunicacao,
            'data_hora': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Define o status operacional do dado inserido e salva no histórico
        leitura['status_operacional'] = status_operacional(leitura)
        historico.append(leitura)
        
        print("Dados registrados com sucesso!")
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos corretos.")

def analisar_dados(leitura):
    """Verifica as condições críticas e retorna uma lista com os alertas ativos."""
    alertas = []
    if leitura['temperatura'] > 80:
        alertas.append("Alerta de superaquecimento")
    if leitura['energia'] < 20:
        alertas.append("Economia de energia")
    if leitura['comunicacao'] == 0:
        alertas.append("Falha de comunicação")
    return alertas

def status_operacional(leitura):
    """
    Avalia a criticidade das variáveis e define o status unificado.
    - 0 alertas ativos: NOMINAL
    - 1 alerta ativo: ATENÇÃO
    - 2 ou mais alertas: CRÍTICO
    """
    alertas = analisar_dados(leitura)
    total_alertas = len(alertas)
    
    if total_alertas == 0:
        return "NOMINAL"
    elif total_alertas == 1:
        return "ATENÇÃO"
    else:
        return "CRÍTICO"

def visualizar_status():
    """Exibe o status consolidado e as métricas da última leitura registrada."""
    print("\n--- Status Atual da Missão ---")
    if not historico:
        print("Nenhum dado registrado até o momento.")
        return

    ultima_leitura = historico[-1]
    alertas = analisar_dados(ultima_leitura)
    status = ultima_leitura.get('status_operacional', status_operacional(ultima_leitura))

    print(f"Data/Hora: {ultima_leitura['data_hora']}")
    print(f"Temperatura: {ultima_leitura['temperatura']}°C")
    print(f"Energia: {ultima_leitura['energia']}%")
    print(f"Comunicação: {'Ok' if ultima_leitura['comunicacao'] == 1 else 'Falha'}")
    print(f"STATUS OPERACIONAL: {status}")

    if alertas:
        print("Alertas Ativos:")
        for alerta in alertas:
            print(f" [!] {alerta}")
    else:
        print("Sistema operando normalmente (Nenhum alerta).")

def executar_analise():
    """Re-analisa o último dado armazenado na memória."""
    print("\n--- Executar Análise ---")
    if not historico:
        print("Nenhum dado registrado para análise.")
        return

    ultima_leitura = historico[-1]
    alertas = analisar_dados(ultima_leitura)
    status = ultima_leitura.get('status_operacional', status_operacional(ultima_leitura))

    print(f"Análise da leitura capturada em {ultima_leitura['data_hora']}:")
    print(f"Status Consolidado: {status}")
    if alertas:
        for alerta in alertas:
            print(f" - {alerta}")
    else:
        print("[OK] Parâmetros de funcionamento normais.")

def exibir_historico():
    """Apresenta a listagem completa de todas as telemetrias armazenadas."""
    print("\n--- Histórico de Leituras ---")
    if not historico:
        print("O histórico está vazio.")
        return

    for i, leitura in enumerate(historico, start=1):
        status = leitura.get('status_operacional', 'N/D')
        print(f"[{i}] {leitura['data_hora']} | Temp: {leitura['temperatura']}°C | "
              f"Energia: {leitura['energia']}% | Comms: {leitura['comunicacao']} | "
              f"Status: {status}")

def menu():
    """Gerencia a interface de interação via terminal."""
    while True:
        print("\n===============================")
        print(" MONITORAMENTO ESPACIAL - MENU ")
        print("===============================")
        print("1. Inserir dados manualmente")
        print("2. Simular dados dos sensores (Auto)")
        print("3. Visualizar status atual")
        print("4. Executar análise")
        print("5. Consultar histórico")
        print("6. Encerrar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            inserir_dados()
        elif opcao == '2':
            simular_dados()
        elif opcao == '3':
            visualizar_status()
        elif opcao == '4':
            executar_analise()
        elif opcao == '5':
            exibir_historico()
        elif opcao == '6':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()