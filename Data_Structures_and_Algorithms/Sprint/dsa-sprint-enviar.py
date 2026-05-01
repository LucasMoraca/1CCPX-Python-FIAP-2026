'''Pré-requisitos:
- Python 3.x
- Bibliotecas: time, datetime (inclusas na instalação padrão do Python, portanto, não é necessário instalá-las)'''

import time
from datetime import datetime

'''Configurações Globais:
- Define as constantes fundamentais do eletroposto comercial.
- Configura a potência de carregamento (Base: GoodWe HCA G2) e as faixas de preço das tarifas.'''

potencia_kw = 11.0
tarifa_base = 1.85
tarifa_pico = 2.50

'''Função exibir_cabecalho:
- Responsável por renderizar a interface de texto inicial do terminal comercial.
- Padroniza a apresentação inicial no console criando linhas separadoras visuais.'''

def exibir_cabecalho():
    print('=' * 50)
    print(" CHARGEGRID INTELLIGENCE - TERMINAL COMERCIAL")
    print('=' * 50)

'''Função validar_entrada_energia:
- Garante a integridade dos dados numéricos inseridos pelo usuário no terminal.
- Utiliza um loop de repetição e tratamento de exceções para exigir um valor entre 0 e 100 kWh.'''

def validar_entrada_energia():
    while True:
        try:
            energia = float(input("Informe a energia desejada para a sessão (em kWh): "))
            if energia > 0 and energia <= 100:
                return energia
            else:
                print("[!] Erro: A energia deve ser maior que 0 e menor que 100 kWh. \n")
        except ValueError:
            print("[!] Erro: Formato inválido. Digite um número (ex: 15.5). \n")

'''Função determinar_tarifa:
- Implementa a regra de negócio central para a precificação dinâmica da recarga.
- Verifica a hora atual do sistema e aplica a tarifa de pico se a recarga ocorrer entre 18h e 21h.'''

def determinar_tarifa():
    hora_atual = datetime.now().hour
    if 18 <= hora_atual <= 21:
        print(f"[*] Horário de Pico detectado ({hora_atual}h). Tarifa dinâmica aplicada.")
        return tarifa_pico, "Pico (Dinâmica)"
    else:
        print(f"[*] Horário Comercial Normal ({hora_atual}h).")
        return tarifa_base, "Normal"

'''Função simular_sessao:
- Emula a entrega progressiva de potência do eletroposto físico para a interface digital.
- Fraciona a energia solicitada em cinco etapas, calculando a porcentagem e simulando o tempo com pausas.'''

def simular_sessao(energia_alvo):
    energia_entregue = 0.0
    passo_kwh = energia_alvo / 5

    while energia_entregue < energia_alvo:
        time.sleep(1)
        energia_entregue += passo_kwh

        if energia_entregue > energia_alvo:
            energia_entregue = energia_alvo

        porcentagem = (energia_entregue / energia_alvo) * 100
        print(f" Carregando... {energia_entregue:.2f} kWh entregues ({porcentagem:.0f}%)")

'''Função gerar_recibo:
- Consolida as informações da operação para fins de faturamento e exibição final ao cliente.
- Cruza a energia solicitada com a tarifa e usa a potência do hardware para estimar o tempo real da recarga.'''

def gerar_recibo(energia, tarifa_valor, tipo_tarifa):
    custo_total = energia * tarifa_valor
    tempo_estimado_minutos = (energia / potencia_kw) * 60

    print("\n" + "=" * 50)
    print(" RECIBO DE RECARGA")
    print("=" * 50)
    print(f" Energia entregue: {energia:.2f} kWh")
    print(f" Tempo estimado real: {tempo_estimado_minutos:.0f} minutos")
    print(f" Tarifa aplicada: R$ {tarifa_valor:.2f} ({tipo_tarifa})")
    print(f" Custo Total: R$ {custo_total:.2f}")
    print("=" * 50 + "\n")

'''Fluxo Principal do Programa (Orquestrador):
- Centraliza a chamada das funções respeitando a sequência lógica de operação comercial do totem.
- O bloco "if __name__ == '__main__':" protege o script, garantindo que rode apenas quando executado diretamente.'''

if __name__ == "__main__":
    exibir_cabecalho()
    kwh_desejado = validar_entrada_energia()
    valor_kwh, tipo_regra = determinar_tarifa()
    simular_sessao(kwh_desejado)
    gerar_recibo(kwh_desejado, valor_kwh, tipo_regra)