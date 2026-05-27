import time
import os
from datetime import datetime
import json

# ==============================================================================
# CONFIGURAÇÕES DO HARDWARE E NEGÓCIO (CHARGEGRID COMERCIAL)
# ==============================================================================
CAPACIDADE_REDE_KW = 22.0       # Limite total da infraestrutura comercial
POTENCIA_GW11K = 11.0           # Potência nominal do carregador GoodWe GW11K-HCA-20
BATERIA_MEDIA_EV_KWH = 50.0     # Bateria média de um EV no mercado (ex: BYD, Leaf)
TARIFA_BASE = 1.85
TARIFA_PICO = 2.50              # Das 18h às 21h
FATOR_SIMULACAO = 1200          # Acelera o tempo no terminal para fins de teste

# ==============================================================================
# CLASSES DE DOMÍNIO
# ==============================================================================
class SessaoRecarga:
    def __init__(self, id_sessao, porcentagem_alvo):
        self.id = id_sessao
        self.porcentagem_alvo = porcentagem_alvo
        # Transforma a porcentagem solicitada em energia (kWh)
        self.energia_alvo = (porcentagem_alvo / 100.0) * BATERIA_MEDIA_EV_KWH
        self.energia_entregue = 0.0
        self.potencia_alocada = POTENCIA_GW11K
        
        self.tempo_inicio = time.time()
        self.ultima_atualizacao = self.tempo_inicio
        
        # Define a tarifa no momento da conexão
        hora = datetime.now().hour
        self.tarifa_valor = TARIFA_PICO if 18 <= hora <= 21 else TARIFA_BASE
        self.tipo_tarifa = "Pico" if 18 <= hora <= 21 else "Normal"

    def calcular_tempo_estimado(self):
        """Calcula o tempo real esperado usando a potência nominal de 11kW do GoodWe"""
        horas_necessarias = self.energia_alvo / POTENCIA_GW11K
        return horas_necessarias * 60 # Retorna em minutos

    def atualizar_consumo(self):
        agora = time.time()
        tempo_horas = ((agora - self.ultima_atualizacao) * FATOR_SIMULACAO) / 3600
        
        self.energia_entregue += self.potencia_alocada * tempo_horas
        if self.energia_entregue > self.energia_alvo:
            self.energia_entregue = self.energia_alvo
            
        self.ultima_atualizacao = agora

class EletropostoComercial:
    def __init__(self):
        self.sessoes = {}
        self.contador = 1
        self.logs_ocpp = []

    def log_ocpp(self, acao, dados):
        """Registra logs compactos de integração para não sujar a tela"""
        msg = f"[OCPP | {datetime.now().strftime('%H:%M:%S')}] {acao} -> {json.dumps(dados)}"
        self.logs_ocpp.append(msg)
        if len(self.logs_ocpp) > 4: # Mantém apenas os 4 últimos logs na tela
            self.logs_ocpp.pop(0)

    def balancear_carga(self):
        """Smart Charging: Limita a potência se houver muitos carros conectados"""
        qtd = len(self.sessoes)
        if qtd == 0: return

        demanda = qtd * POTENCIA_GW11K
        nova_potencia = CAPACIDADE_REDE_KW / qtd if demanda > CAPACIDADE_REDE_KW else POTENCIA_GW11K

        for sessao in self.sessoes.values():
            sessao.atualizar_consumo()
            sessao.potencia_alocada = nova_potencia

        self.log_ocpp("LoadBalancing", {"active": qtd, "limitKw": round(nova_potencia, 2)})

    def iniciar_sessao(self, porcentagem):
        id_sessao = f"S-{self.contador:03d}"
        nova_sessao = SessaoRecarga(id_sessao, porcentagem)
        self.sessoes[id_sessao] = nova_sessao
        self.contador += 1
        
        minutos_estimados = nova_sessao.calcular_tempo_estimado()
        
        self.log_ocpp("StartTx", {"id": id_sessao, "target%": porcentagem})
        self.balancear_carga()
        
        return id_sessao, minutos_estimados

    def finalizar_sessao(self, id_sessao):
        if id_sessao not in self.sessoes:
            return None
            
        sessao = self.sessoes.pop(id_sessao)
        sessao.atualizar_consumo()
        self.balancear_carga()
        
        self.log_ocpp("StopTx", {"id": id_sessao, "kwh": round(sessao.energia_entregue, 2)})
        return sessao

# ==============================================================================
# INTERFACE DE USUÁRIO (MENU LIMPO)
# ==============================================================================
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_painel(sistema):
    limpar_tela()
    print("=" * 65)
    print(" ⚡ CHARGEGRID INTELLIGENCE - PAINEL COMERCIAL")
    print("=" * 65)
    
    if sistema.logs_ocpp:
        print("\n--- STATUS DE INTEGRAÇÃO (ÚLTIMOS PACOTES OCPP) ---")
        for log in sistema.logs_ocpp:
            print(log)
            
    print("\n--- SESSÕES ATIVAS ---")
    if not sistema.sessoes:
        print(" Nenhum veículo conectado.")
    else:
        print(f"{'ID':<8} | {'OBJETIVO':<10} | {'PROGRESSO':<12} | {'POTÊNCIA':<9} | {'TARIFA':<8} | {'CUSTO (R$)'}")
        print("-" * 65)
        for id_sessao, s in sistema.sessoes.items():
            s.atualizar_consumo()
            progresso_pct = (s.energia_entregue / s.energia_alvo) * s.porcentagem_alvo if s.energia_alvo > 0 else 0
            custo = s.energia_entregue * s.tarifa_valor
            
            # Formatação tabular limpa
            print(f"{id_sessao:<8} | {s.porcentagem_alvo:>3}% ({s.energia_alvo:>4.1f}kWh)| "
                  f"{progresso_pct:>5.1f}% ({s.energia_entregue:>4.1f}k) | {s.potencia_alocada:>5.1f} kW | "
                  f"{s.tipo_tarifa:<8} | R$ {custo:>5.2f}")
    
    print("=" * 65)

def menu_principal():
    sistema = EletropostoComercial()
    
    while True:
        exibir_painel(sistema)
        print("\n[1] Conectar Veículo")
        print("[2] Atualizar Painel")
        print("[3] Desconectar Veículo")
        print("[0] Desligar Terminal")
        
        opcao = input("\nSelecione uma ação: ")
        
        if opcao == '1':
            try:
                pct = float(input("\nQual a porcentagem desejada de carga? (1 a 100): "))
                if 1 <= pct <= 100:
                    id_s, tempo = sistema.iniciar_sessao(pct)
                    input(f"\n[+] Veículo conectado! Sessão {id_s} iniciada.\nTempo médio estimado (11kW): {tempo:.0f} minutos.\nPressione ENTER para continuar...")
                else:
                    input("\n[!] Valor inválido. A porcentagem deve ser entre 1 e 100. Pressione ENTER...")
            except ValueError:
                input("\n[!] Digite apenas números. Pressione ENTER...")
                
        elif opcao == '2':
            continue # O loop já redesenha a tela atualizada
            
        elif opcao == '3':
            id_alvo = input("\nDigite o ID da sessão (ex: S-001): ").strip().upper()
            recibo = sistema.finalizar_sessao(id_alvo)
            if recibo:
                custo_total = recibo.energia_entregue * recibo.tarifa_valor
                print(f"\n=== RECIBO - {id_alvo} ===")
                print(f"Energia consumida: {recibo.energia_entregue:.2f} kWh")
                print(f"Tarifa ({recibo.tipo_tarifa}): R$ {recibo.tarifa_valor:.2f} / kWh")
                print(f"Total a pagar: R$ {custo_total:.2f}")
                print("===========================")
                input("\nPressione ENTER para fechar o recibo e voltar ao painel...")
            else:
                input("\n[!] Sessão não encontrada. Pressione ENTER...")
                
        elif opcao == '0':
            limpar_tela()
            print("Sistema encerrado com segurança.")
            break

if __name__ == "__main__":
    menu_principal()