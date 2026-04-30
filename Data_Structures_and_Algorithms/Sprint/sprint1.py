# importando a biblioteca que lidará com funções relacionadas ao tempo. Criará uma pausa e simula a passagem de tempo durante a recarga.
import time
# importando o módulo datetime para capturar datas e horas exatas do sistema
from datetime import datetime

# Construindo as configurações de eletroposto (Base: GoodWe HCA G2)
potencia_kw = 11.0  # Potência de carregamento em kW
tarifa_base = 1.85  # R$ por kWh
tarifa_pico = 2.50  # R$ por kWh (Horário de pico comercial)


# Funções de Interface e validação

# Cria (define) uma função que imprime o título do programa.
def exibir_cabecalho():
    print(
        '=' * 50)  # Uma técnica legal do Python que imprime o sinal de igual = 50 vezes seguidas, criando uma linha separadora visual.
    print(" CHARGEGRID INTELLIGENCE - TERMINAL COMERCIAL")
    print('=' * 50)


# Define a função que vai perguntar ao usuário quanta energia ele quer.
def validar_entrada_energia():
    """Uso de estrutura de repetição (While) para validar a entrada de dados."""
    while True:  # Inicia um "loop infinito". Ele só vai parar quando encontrar a instrução return. Isso garante que o programa fique pedindo a energia até o usuário digitar um valor válido.
        try:  # Tenta executar o bloco de código abaixo. É usado para prevenir que o programa quebre se o usuário digitar texto em vez de números.
            energia = float(input("Informe a energia desejada para a sessão (em kWh): "))
            if energia > 0 and energia <= 100:  # Verifica se a energia pedida é um valor lógico (maior que zero e no máximo 100). Limite de segurança de bateria comum
                return energia  # Se o valor for válido, ele encerra a função e devolve o valor de energia para ser usado no resto do programa (quebrando o loop while True).
            else:  # Se o número for menor ou igual a 0, ou maior que 100, executa a linha de baixo.
                print("[!] Erro: A energia deve ser maior que 0 e menor que 100 kWh. \n")
        except ValueError:  # Se o usuário digitou letras (ex: "dez") e o float() falhou, o Python não "quebra", ele cai aqui neste bloco e exibe a mensagem de erro da linha seguinte.
            print("[!] Erro: Formato inválido. Digite um número (ex: 15.5). \n")


# Regras de Negócio e Simulação

def determinar_tarifa():  # Função que decide qual preço cobrar baseado na hora do dia.
    """Uso de estruturas condicionais (IF/ELSE) para precificação dinâmica."""
    hora_atual = datetime.now().hour  # O método datetime.now() pega a data e hora exatas de agora, e o .hour extrai apenas o número da hora (de 0 a 23).
    # Simulação de horário de pico (ex: 18h às 21h)
    if 18 <= hora_atual <= 21:
        print(f"[*] Horário de Pico detectado ({hora_atual}h). Tarifa dinâmica aplicada.")
        return tarifa_pico, "Pico (Dinâmica)"
    else:  # e o bloco abaixo: Caso não seja horário de pico, devolve a TARIFA_BASE e a string "Normal".
        print(f"[*] Horário Comercial Normal ({hora_atual}h).")
        return tarifa_base, "Normal"


# Esta função recebe como parâmetro a quantidade de energia que o usuário pediu (energia_alvo).
def simular_sessao(energia_alvo):
    """Uso de repetição (WHILE) para simular a passagem do tempo e entrega de kWh. """
    energia_entregue = 0.0  # Cria uma variável começando do zero para controlar quanto já foi "carregado".

    passo_kwh = energia_alvo / 5  # Divide a simulação em 5 etapas

    while energia_entregue < energia_alvo:  # Inicia um loop que continua rodando enquanto a energia entregue for menor que a pedida.
        time.sleep(1)  # Pausa de 1 segundo para simular o tempo real
        energia_entregue += passo_kwh  # Adiciona o "passo" à energia que já foi entregue (equivalente a energia_entregue = energia_entregue + passo_kwh).

        # Garante que não ultrapasse o alvo devido a arredondamentos
        if energia_entregue > energia_alvo:
            energia_entregue = energia_alvo

        # Regra de três simples para calcular a porcentagem concluída.
        porcentagem = (energia_entregue / energia_alvo) * 100
        print(f" Carregando... {energia_entregue:.2f} kWh entregues ({porcentagem:.0f}%)")


# Faturamento e Fluxo Principal

# Função que recebe três argumentos para montar a nota fiscal.
def gerar_recibo(energia, tarifa_valor, tipo_tarifa):
    """Cálculo de tarifação e saída formatada."""

    custo_total = energia * tarifa_valor  # Multiplica os kWh consumidos pelo preço da tarifa decidida anteriormente.

    tempo_estimado_minutos = (
                                         energia / potencia_kw) * 60  # Calcula quanto tempo um carregador com essa potência demoraria na vida real para entregar essa energia, convertendo de horas para minutos (multiplicando por 60).

    # Adicionadas linhas de print para exibir o recibo final
    print("\n" + "=" * 50)
    print(" RECIBO DE RECARGA")
    print("=" * 50)
    print(f" Energia entregue: {energia:.2f} kWh")
    print(f" Tempo estimado real: {tempo_estimado_minutos:.0f} minutos")
    print(f" Tarifa aplicada: R$ {tarifa_valor:.2f} ({tipo_tarifa})")
    print(f" Custo Total: R$ {custo_total:.2f}")
    print("=" * 50 + "\n")


# Fluxo Principal do Programa (Indentação corrigida para fora da função gerar_recibo)
if __name__ == "__main__":  # Esta é uma proteção clássica do Python. Ela verifica se o arquivo está sendo rodado diretamente (por exemplo, você clicou nele ou chamou no terminal). Se este arquivo fosse importado por um outro script, as funções existiriam, mas o código abaixo não rodaria automaticamente.

    exibir_cabecalho()

    # 1. Entrada de Dados
    kwh_desejado = validar_entrada_energia()

    # 2. Decisão de Tarifação
    valor_kwh, tipo_regra = determinar_tarifa()

    # 3. Execução da Sessão
    simular_sessao(kwh_desejado)

    # 4. Encerramento e Faturamento
    gerar_recibo(kwh_desejado, valor_kwh, tipo_regra)