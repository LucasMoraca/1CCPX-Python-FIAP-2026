import time
from datetime import datetime

# Configurações do Negócio
POTENCIA_GW11K = 11.0
TARIFA_BASE = 1.85
TARIFA_PICO = 2.50

class Sessao:
    def __init__(self, id_sessao, energia_alvo):
        self.id = id_sessao
        self.energia = energia_alvo
        self.tempo = (energia_alvo / POTENCIA_GW11K) * 60
        
        hora = datetime.now().hour
        self.tarifa = TARIFA_PICO if 18 <= hora <= 21 else TARIFA_BASE
        self.custo = self.energia * self.tarifa

def cadastrar_sessao(sessoes, contador):
    try:
        energia = float(input("Energia consumida (kWh): "))
        if energia <= 0:
            print("A energia deve ser maior que zero.")
            return contador
        
        id_sessao = f"S-{contador:03d}"
        nova_sessao = Sessao(id_sessao, energia)
        sessoes.append(nova_sessao)
        print(f"\nSessão {id_sessao} cadastrada com sucesso!")
        return contador + 1
    except ValueError:
        print("Valor inválido. Digite apenas números.")
        return contador

def listar_sessoes(sessoes):
    if not sessoes:
        print("Nenhuma sessão cadastrada.")
        return
    print(f"{'ID':<8} | {'ENERGIA':<10} | {'TEMPO':<10} | {'CUSTO'}")
    for s in sessoes:
        print(f"{s.id:<8} | {s.energia:>6.1f} kWh | {s.tempo:>7.1f} m | R$ {s.custo:.2f}")

def busca_sequencial(sessoes, id_procurado):
    for i in range(len(sessoes)):
        if sessoes[i].id == id_procurado:
            return sessoes[i]
    return None

def bubble_sort_custo(sessoes):
    n = len(sessoes)
    for i in range(n):
        for j in range(n - 1 - i):
            if sessoes[j].custo > sessoes[j + 1].custo:
                sessoes[j], sessoes[j + 1] = sessoes[j + 1], sessoes[j]
    print("\nSessões ordenadas por custo com sucesso!")

def mostrar_estatisticas(sessoes):
    if not sessoes:
        print("Sem dados para estatísticas.")
        return
    
    total_sessoes = len(sessoes)
    energia_total = sum(s.energia for s in sessoes)
    faturamento = sum(s.custo for s in sessoes)
    maior_consumo = sessoes[0].energia
    menor_consumo = sessoes[0].energia

    for s in sessoes:
        if s.energia > maior_consumo: maior_consumo = s.energia
        if s.energia < menor_consumo: menor_consumo = s.energia

    print("\n========= ESTATÍSTICAS ==========")
    print(f"Sessões realizadas: {total_sessoes}")
    print(f"Energia fornecida: {energia_total:.2f} kWh")
    print(f"Faturamento: R$ {faturamento:.2f}")
    print(f"Ticket médio: R$ {(faturamento/total_sessoes):.2f}")
    print(f"Maior consumo: {maior_consumo:.2f} kWh")
    print(f"Menor consumo: {menor_consumo:.2f} kWh")

def menu_principal():
    sessoes = []
    contador = 1
    
    while True:
        print("\n=====================================")
        print("        ESTAÇÃO DE RECARGA")
        print("=====================================")
        print("1 - Nova sessão de recarga")
        print("2 - Listar sessões")
        print("3 - Buscar sessão (por ID)")
        print("4 - Ordenar sessões (por Custo)")
        print("5 - Estatísticas")
        print("6 - Encerrar")
        
        opcao = input("\nEscolha: ")
        
        if opcao == '1':
            contador = cadastrar_sessao(sessoes, contador)
        elif opcao == '2':
            listar_sessoes(sessoes)
        elif opcao == '3':
            id_buscado = input("Digite o ID (ex: S-001): ").strip().upper()
            resultado = busca_sequencial(sessoes, id_buscado)
            if resultado:
                print(f"\nSessão Encontrada: Energia {resultado.energia}kWh, Custo R${resultado.custo:.2f}")
            else:
                print("\nSessão não encontrada.")
        elif opcao == '4':
            bubble_sort_custo(sessoes)
        elif opcao == '5':
            mostrar_estatisticas(sessoes)
        elif opcao == '6':
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()
    