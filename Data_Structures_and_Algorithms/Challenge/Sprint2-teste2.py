import time
import os
import json
import csv
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
        self.status = "Carregando"
        
        # Variáveis de tarifação dinâmica
        self.custo_acumulado = 0.0
        self.energia_pico = 0.0
        self.energia_normal = 0.0
        self.custo_pico = 0.0
        self.custo_normal = 0.0

    def obter_tarifa_atual(self):
        """Retorna o valor da tarifa e o tipo baseado na hora atual do sistema."""
        hora_atual = datetime.now().hour
        if 18 <= hora_atual <= 21:
            return TARIFA_PICO, "Pico"
        return TARIFA_BASE, "Normal"

    def calcular_tempo_estimado(self):
        horas_necessarias = self.energia_alvo / POTENCIA_GW11K
        return horas_necessarias * 60 

    def atualizar_consumo(self):
        """Calcula o consumo e custo fracionado dinamicamente com base no tempo decorrido."""
        if self.status != "Carregando":
            return

        agora = time.time()
        tempo_horas = ((agora - self.ultima_atualizacao) * FATOR_SIMULACAO) / 3600
        
        # Energia fornecida neste delta de tempo
        energia_delta = self.potencia_alocada * tempo_horas
        
        # Impede que ultrapasse o alvo
        if self.energia_entregue + energia_delta >= self.energia_alvo:
            energia_delta = self.energia_alvo - self.energia_entregue
            self.status = "Concluida"
            
        # Calcula custo dinâmico
        tarifa_vigente, tipo_tarifa = self.obter_tarifa_atual()
        custo_delta = energia_delta * tarifa_vigente

        # Acumula totais
        self.energia_entregue += energia_delta
        self.custo_acumulado += custo_delta
        
        if tipo_tarifa == "Pico":
            self.energia_pico += energia_delta
            self.custo_pico += custo_delta
        else:
            self.energia_normal += energia_delta
            self.custo_normal += custo_delta
            
        self.ultima_atualizacao = agora

    def encerrar_sessao(self):
        """Trava os valores finais para evitar flutuações após o encerramento."""
        self.atualizar_consumo()
        self.status = "Encerrada"
        return self

class EletropostoComercial:
    def __init__(self):
        self.sessoes = {}
        self.historico_sessoes = []  # Armazena sessões finalizadas para relatórios
        self.contador = 1
        self.logs_ocpp = []

    def simular_integracao(self, acao, dados):
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
        self.historico_sessoes.append(sessao) # Salva no histórico para o relatório
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
    print("=" * 85)
    print(" ⚡ CHARGEGRID INTELLIGENCE - PAINEL COMERCIAL")
    print("=" * 85)
    
    if sistema.logs_ocpp:
        print("\n--- STATUS DE INTEGRAÇÃO (ÚLTIMOS PACOTES OCPP) ---")
        for log in sistema.logs_ocpp:
            print(log)
            
    print("\n--- SESSÕES ATIVAS ---")
    if not sistema.sessoes:
        print(" Nenhum veículo conectado.")
    else:
        print(f"{'ID':<6} | {'PROGRESSO':<12} | {'ENTREGUE':<10} | {'POTÊNCIA':<9} | {'TARIFA ATUAL':<12} | {'CUSTO (R$)'}")
        print("-" * 85)
        for id_sessao, s in sistema.sessoes.items():
            s.atualizar_consumo()
            
            progresso_pct = (s.energia_entregue / s.energia_alvo) * 100 if s.energia_alvo > 0 else 0
            potencia_display = 0.0 if s.status == "Concluida" else s.potencia_alocada
            _, tipo_tarifa_atual = s.obter_tarifa_atual()
            
            print(f"{id_sessao:<6} | {progresso_pct:>5.1f}% / 100% | {s.energia_entregue:>4.1f} kWh   | {potencia_display:>5.1f} kW | "
                  f"{tipo_tarifa_atual:<12} | R$ {s.custo_acumulado:>5.2f}")
    
    print("=" * 85)

def gerenciar_relatorios(sistema):
    limpar_tela()
    print("=" * 70)
    print(" 📊 RELATÓRIO CONSOLIDADO DE OPERAÇÃO")
    print("=" * 70)
    
    if not sistema.historico_sessoes:
        print("\nNenhuma sessão foi finalizada ainda para gerar relatório.")
        print("\n" + "=" * 70)
        input("Pressione ENTER para voltar...")
        return

    total_sessoes = len(sistema.historico_sessoes)
    total_kwh = sum(s.energia_entregue for s in sistema.historico_sessoes)
    total_kwh_pico = sum(s.energia_pico for s in sistema.historico_sessoes)
    total_kwh_normal = sum(s.energia_normal for s in sistema.historico_sessoes)
    total_arrecadado = sum(s.custo_acumulado for s in sistema.historico_sessoes)
    
    print(f"Total de Sessões Finalizadas: {total_sessoes}")
    print(f"Total de Energia Fornecida:   {total_kwh:.2f} kWh")
    print(f"  - Energia em Horário Pico:  {total_kwh_pico:.2f} kWh")
    print(f"  - Energia em Horário Base:  {total_kwh_normal:.2f} kWh")
    print(f"Total Arrecadado Bruto:       R$ {total_arrecadado:.2f}")
    print("=" * 70)
    
    print("\nOpções de Exportação:")
    print("[1] Exportar como CSV")
    print("[2] Exportar como JSON")
    print("[0] Voltar ao Menu Principal")
    
    opcao = input("\nSelecione: ")
    
    dados_exportacao = []
    for s in sistema.historico_sessoes:
        dados_exportacao.append({
            "id_sessao": s.id,
            "energia_total_kwh": round(s.energia_entregue, 2),
            "energia_pico_kwh": round(s.energia_pico, 2),
            "energia_normal_kwh": round(s.energia_normal, 2),
            "custo_total_brl": round(s.custo_acumulado, 2)
        })

    if opcao == '1':
        arquivo = f"relatorio_chargegrid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(arquivo, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=dados_exportacao[0].keys())
            writer.writeheader()
            writer.writerows(dados_exportacao)
        print(f"\n[+] Relatório exportado com sucesso: {arquivo}")
        input("Pressione ENTER para voltar...")
        
    elif opcao == '2':
        arquivo = f"relatorio_chargegrid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(arquivo, 'w') as f:
            json.dump({"resumo_geral": {"total_sessoes": total_sessoes, "total_kwh": round(total_kwh, 2), "total_arrecadado": round(total_arrecadado, 2)}, "sessoes": dados_exportacao}, f, indent=4)
        print(f"\n[+] Relatório exportado com sucesso: {arquivo}")
        input("Pressione ENTER para voltar...")

def menu_principal():
    sistema = EletropostoComercial()
    
    while True:
        exibir_painel(sistema)
        print("\n[1] Conectar Veículo")
        print("[2] Atualizar Painel")
        print("[3] Desconectar Veículo")
        print("[4] Relatórios e Exportação")
        print("[0] Desligar Terminal")
        
        opcao = input("\nSelecione uma ação: ")
        
        if opcao == '1':
            try:
                pct = float(input("\nQual a porcentagem desejada de carga? (1 a 100): "))
                if 1 <= pct <= 100:
                    id_s, tempo = sistema.iniciar_sessao(pct)
                    print(f"\n[+] Veículo conectado! Sessão {id_s} iniciada.")
                    print(f"Tempo médio estimado (11kW): {tempo:.0f} minutos.")
                    input("Pressione ENTER para continuar...")
                else:
                    input("\n[!] Valor inválido. A porcentagem deve ser entre 1 e 100. Pressione ENTER...")
            except ValueError:
                input("\n[!] Digite apenas números. Pressione ENTER...")
                
        elif opcao == '2':
            continue 
            
        elif opcao == '3':
            id_alvo = input("\nDigite o ID da sessão (ex: S-001): ").strip().upper()
            recibo = sistema.finalizar_sessao(id_alvo)
            if recibo:
                print(f"\n=== RECIBO - {id_alvo} ===")
                print(f"Energia consumida: {recibo.energia_entregue:.2f} kWh")
                print(f"  - Em horário de Pico: {recibo.energia_pico:.2f} kWh")
                print(f"  - Em horário Base:    {recibo.energia_normal:.2f} kWh")
                print(f"Total pago: R$ {recibo.custo_acumulado:.2f}")
                print("===========================")
                input("\nPressione ENTER para fechar o recibo e voltar ao painel...")
            else:
                input("\n[!] Sessão não encontrada. Pressione ENTER...")
                
        elif opcao == '4':
            gerenciar_relatorios(sistema)

        elif opcao == '0':
            limpar_tela()
            print("Sistema encerrado com segurança.")
            break

if __name__ == "__main__":
    menu_principal()