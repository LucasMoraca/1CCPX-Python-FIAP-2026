import os
import time
from datetime import datetime

historico = []

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def cor(texto, codigo):
    return f"\033[{codigo}m{texto}\033[0m"

def inserir_dados():
    print("\n=== Inserir Dados da Missão ===")
    try:
        temperatura = float(input("Temperatura da nave: "))
        energia = float(input("Energia (%): "))
        comunicacao = int(input("Status da comunicação (1 = ok, 0 = falha): "))

        leitura = {
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "temperatura": temperatura,
            "energia": energia,
            "comunicacao": comunicacao
        }

        historico.append(leitura)
        print(cor("Leitura cadastrada com sucesso!", "32"))
    except ValueError:
        print(cor("Erro: digite valores válidos.", "31"))

def analisar_dados(leitura):
    alertas = []

    if leitura["temperatura"] > 80:
        alertas.append("Alerta de superaquecimento")

    if leitura["energia"] < 20:
        alertas.append("Economia de energia")

    if leitura["comunicacao"] == 0:
        alertas.append("Falha de comunicação")

    if not alertas:
        alertas.append("Sistema operando normalmente")

    return alertas

def visualizar_status():
    print("\n=== Status Atual da Missão ===")
    if not historico:
        print(cor("Nenhuma leitura registrada ainda.", "33"))
        return

    leitura = historico[-1]
    print(f"Data/Hora: {leitura['data_hora']}")
    print(f"Temperatura: {leitura['temperatura']}°C")
    print(f"Energia: {leitura['energia']}%")
    print(f"Comunicação: {'OK' if leitura['comunicacao'] == 1 else 'FALHA'}")

    alertas = analisar_dados(leitura)
    print("\nAlertas:")
    for alerta in alertas:
        if "Falha" in alerta or "superaquecimento" in alerta:
            print(cor(f"- {alerta}", "31"))
        elif "Economia" in alerta:
            print(cor(f"- {alerta}", "33"))
        else:
            print(cor(f"- {alerta}", "32"))

def executar_analise():
    print("\n=== Análise da Missão ===")
    if not historico:
        print(cor("Nenhuma leitura disponível para análise.", "33"))
        return

    leitura = historico[-1]
    alertas = analisar_dados(leitura)

    print("Resultado da análise:")
    for alerta in alertas:
        print(f"- {alerta}")

def mostrar_historico():
    print("\n=== Histórico de Leituras ===")
    if not historico:
        print(cor("Sem registros no histórico.", "33"))
        return

    for i, leitura in enumerate(historico, start=1):
        print(f"\nLeitura {i}")
        print(f"Data/Hora: {leitura['data_hora']}")
        print(f"Temperatura: {leitura['temperatura']}°C")
        print(f"Energia: {leitura['energia']}%")
        print(f"Comunicação: {'OK' if leitura['comunicacao'] == 1 else 'FALHA'}")

def simular_dados():
    import random
    temperatura = random.randint(50, 100)
    energia = random.randint(0, 100)
    comunicacao = random.randint(0, 1)

    leitura = {
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "temperatura": temperatura,
        "energia": energia,
        "comunicacao": comunicacao
    }

    historico.append(leitura)
    print(cor("Leitura simulada adicionada.", "32"))

def menu():
    while True:
        print("\n" + "=" * 40)
        print(cor("SISTEMA DE MONITORAMENTO ESPACIAL", "36"))
        print("=" * 40)
        print("1. Inserir dados")
        print("2. Visualizar status")
        print("3. Executar análise")
        print("4. Histórico das leituras")
        print("5. Simular dados")
        print("6. Encerrar sistema")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            inserir_dados()
        elif opcao == "2":
            visualizar_status()
        elif opcao == "3":
            executar_analise()
        elif opcao == "4":
            mostrar_historico()
        elif opcao == "5":
            simular_dados()
        elif opcao == "6":
            print(cor("Encerrando sistema...", "36"))
            break
        else:
            print(cor("Opção inválida. Tente novamente.", "31"))

        time.sleep(1)

if __name__ == "__main__":
    menu()