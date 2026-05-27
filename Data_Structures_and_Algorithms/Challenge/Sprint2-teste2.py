import time
import os
import json
import random
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÕES DO HARDWARE E NEGÓCIO (CHARGEGRID COMERCIAL)
# ==============================================================================
CAPACIDADE_REDE_KW = 22.0       # Limite total da infraestrutura comercial
POTENCIA_GW11K = 11.0           # Potência nominal do carregador GoodWe GW11K-HCA-20
BATERIA_MEDIA_EV_KWH = 50.0     # Bateria média de um EV no mercado
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
        self.energia_alvo = (porcentagem_alvo / 100.0) * BATERIA_MEDIA_EV_KWH
        self.energia_entregue = 0.0
        self.potencia_alocada = POTENCIA_GW11K
        
        self.tempo_inicio = time.time()
        self.ultima_atualizacao = self.tempo_inicio
        self.custo_final = 0.0
        self.status = "Carregando"
        
        hora = datetime.now().hour
        self.tarifa_valor = TARIFA_PICO if 18 <= hora <= 21 else TARIFA_BASE
        self.tipo_tarifa = "Pico" if 18 <= hora <= 21 else "Normal"

    def calcular_tempo_estimado(self):
        horas_necessarias = self.energia_alvo / POTENCIA_GW11K
        return horas_necessarias * 60 

    def atualizar_consumo(self):
        if self.status != "Carregando":
            return

        agora = time.time()
        tempo_horas = ((agora - self.ultima_atualizacao) * FATOR_SIMULACAO) / 3600
        
        self.energia_entregue += self.potencia_alocada * tempo_horas
        if self.energia_entregue >= self.energia_alvo:
            self.energia_entregue = self.energia_alvo
            self.status = "Concluida"
            
        self.ultima_atualizacao = agora

    def encerrar_sessao(self):
        """Trava os valores finais para evitar flutuações após o encerramento."""
        self.atualizar_consumo()
        self.custo_final = self.energia_entregue * self.tarifa_valor
        self.status = "Encerrada"
        return self.custo_final

class EletropostoComercial:
    def __init__(self):
        self.sessoes = {}
        self.contador = 1
        self.logs_ocpp = []

    def simular_integracao(self, acao, dados):
        """Simula estrutura JSON OCPP/MODBUS e resposta ACK do servidor."""
        msg_id = f"MSG-{random.randint(1000, 9999)}"
        pacote_tx = {
            "messageId": msg_id,
            "action": acao,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "payload": dados
        }
        
        self.logs_ocpp.append(f"[TX_REQ] {json.dumps(pacote_tx)}")
        self.logs_ocpp.append(f"[RX_ACK] Plataforma confirmou {msg_id} (Status: Accepted)")
        
        if len(self.logs_ocpp) > 6:
            self.logs_ocpp = self.logs_ocpp[-6:]

    def balancear_carga(self):
        qtd = len([s for s in self.sessoes.values() if s.status == "Carregando"])
        if qtd == 0: 
            return

        demanda = qtd * POTENCIA_GW11K
        nova_potencia = CAPACIDADE_REDE_KW / qtd if demanda > CAPACIDADE_REDE_KW else POTENCIA_GW11K

        for sessao in self.sessoes.values():
            if sessao.status == "Carregando":
                sessao.atualizar_consumo()
                sessao.potencia_alocada = nova_potencia

        self.simular_integracao("LoadBalancing", {
            "activeSessions": qtd, 
            "powerLimitKw": round(nova_potencia, 2)
        })

    def iniciar_sessao(self, porcentagem):
        id_sessao = f"S-{self.contador:03d}"
        nova_sessao = SessaoRecarga(id_sessao, porcentagem)
        self.sessoes[id_sessao] = nova_sessao
        self.contador += 1
        
        minutos_estimados = nova_sessao.calcular_tempo_estimado()
        
        self.simular_integracao("StartTransaction", {
            "sessionId": id_sessao,
            "meterValue": 0,
            "powerLimit": nova_sessao.potencia_alocada,
            "status": nova_sessao.status
        })
        self.balancear_carga()
        
        return id_sessao, minutos_estimados

    def finalizar_sessao(self, id_sessao):
        if id_sessao not in self.sessoes:
            return None
            
        sessao = self.sessoes.pop(id_sessao)
        sessao.encerrar_sessao()
        self.balancear_carga()
        
        self.simular_integracao("StopTransaction", {
            "sessionId": id_sessao,
            "meterValue": round(sessao.energia_entregue, 2),
            "status": sessao.status
        })
        return sessao

# ==============================================================================
# INTERFACE DE USUÁRIO (MENU COMERCIAL LIMPO)
# ==============================================================================
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_painel(sistema):
    limpar_tela()
    print("=" * 70)
    print(" ⚡ CHARGEGRID INTELLIGENCE - PAINEL COMERCIAL")
    print("=" * 70)
    
    if sistema.logs_ocpp:
        print()
        print("--- STATUS DE INTEGRAÇÃO (ÚLTIMOS PACOTES OCPP) ---")
        for log in sistema.logs_ocpp:
            print(log)
            
    print()
    print("--- SESSÕES ATIVAS ---")
    if not sistema.sessoes:
        print(" Nenhum veículo conectado.")
    else:
        print(f"{'ID':<8} | {'PROGRESSO':<12} | {'ENTREGUE':<10} | {'POTÊNCIA':<9} | {'TARIFA':<8} | {'CUSTO (R$)'}")
        print("-" * 70)
        for id_sessao, s in sistema.sessoes.items():
            s.atualizar_consumo()
            
            progresso_pct = (s.energia_entregue / s.energia_alvo) * 100 if s.energia_alvo > 0 else 0
            custo_parcial = s.energia_entregue * s.tarifa_valor
            
            potencia_display = 0.0 if s.status == "Concluida" else s.potencia_alocada
            
            print(f"{id_sessao:<8} | {progresso_pct:>5.1f}% / 100% | {s.energia_entregue:>4.1f} kWh   | {potencia_display:>5.1f} kW | "
                  f"{s.tipo_tarifa:<8} | R$ {custo_parcial:>5.2f}")
    
    print("=" * 70)

def menu_principal():
    sistema = EletropostoComercial()
    
    while True:
        exibir_painel(sistema)
        print()
        print("[1] Conectar Veículo")
        print("[2] Atualizar Painel")
        print("[3] Desconectar Veículo")
        print("[0] Desligar Terminal")
        
        print()
        opcao = input("Selecione uma ação: ")
        
        if opcao == '1':
            print()
            try:
                pct = float(input("Qual a porcentagem desejada de carga? (1 a 100): "))
                if 1 <= pct <= 100:
                    id_s, tempo = sistema.iniciar_sessao(pct)
                    print()
                    print(f"[+] Veículo conectado! Sessão {id_s} iniciada.")
                    print(f"Tempo médio estimado (11kW): {tempo:.0f} minutos.")
                    input("Pressione ENTER para continuar...")
                else:
                    print()
                    input("[!] Valor inválido. A porcentagem deve ser entre 1 e 100. Pressione ENTER...")
            except ValueError:
                print()
                input("[!] Digite apenas números. Pressione ENTER...")
                
        elif opcao == '2':
            continue 
            
        elif opcao == '3':
            print()
            id_alvo = input("Digite o ID da sessão (ex: S-001): ").strip().upper()
            recibo = sistema.finalizar_sessao(id_alvo)
            if recibo:
                print()
                print(f"=== RECIBO - {id_alvo} ===")
                print(f"Energia consumida: {recibo.energia_entregue:.2f} kWh")
                print(f"Tarifa ({recibo.tipo_tarifa}): R$ {recibo.tarifa_valor:.2f} / kWh")
                print(f"Total pago: R$ {recibo.custo_final:.2f}")
                print("===========================")
                print()
                input("Pressione ENTER para fechar o recibo e voltar ao painel...")
            else:
                print()
                input("[!] Sessão não encontrada. Pressione ENTER...")
                
        elif opcao == '0':
            limpar_tela()
            print("Sistema encerrado com segurança.")
            break

if __name__ == "__main__":
    menu_principal()