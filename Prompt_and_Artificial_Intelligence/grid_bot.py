import time
from datetime import datetime

class GRIDIntelligenceV3:
    def __init__(self):
        # Configurações de Hardware (GoodWe HCA G2)
        self.potencia_kw = 11.0 
        self.tarifa_base = 1.85
        self.tarifa_pico = 2.50
        self.versao = "3.0.0"
        
        # Base de Conhecimento (Requisitos Fase 1)
        self.faq = {
            "balanceamento": "O sistema executa balanceamento dinâmico para evitar sobrecargas na rede local.",
            "historico": "Os ciclos são registrados na nuvem GoodWe e podem ser acessados pelo painel do gestor.",
            "resiliencia": "Em caso de queda de rede, o buffer local armazena os dados até a reconexão.",
            "seguranca": "Monitoramos kWh, tempo e temperatura para garantir a integridade da bateria."
        }

    def log(self, mensagem):
        print(f"\n[GRID]: {mensagem}")

    def identificar_horario_e_tarifa(self):
        """Aplica lógica de precificação dinâmica baseada na hora atual."""
        hora = datetime.now().hour
        if 18 <= hora <= 21:
            return self.tarifa_pico, "Pico (Demanda Alta)"
        return self.tarifa_base, "Normal (Base)"

    def processar_pagamento_e_carga(self):
        """Integra a lógica de faturamento solicitada."""
        self.log("Iniciando módulo de tarifação e carga.")
        
        try:
            kwh_desejado = float(input(">> Informe a quantidade de kWh para carregar (Máx 100): "))
            
            if kwh_desejado <= 0 or kwh_desejado > 100:
                self.log("ERRO: Valor fora dos parâmetros de segurança (1-100kWh).")
                return

            tarifa, tipo = self.identificar_horario_e_tarifa()
            custo_total = kwh_desejado * tarifa
            tempo_minutos = (kwh_desejado / self.potencia_kw) * 60

            self.log(f"Orquestrando carga... Estimativa: {tempo_minutos:.0f} minutos.")
            
            # Simulação de progresso (DSA Sprint)
            for i in range(1, 6):
                time.sleep(0.5)
                progresso = i * 20
                print(f"   [Carga: {progresso}%] Entregando potência GoodWe...")

            # Geração de Recibo Completo
            print("\n" + "="*45)
            print("       EXTRATO DE OPERAÇÃO - GOODWE")
            print("="*45)
            print(f"Data/Hora:     {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            print(f"Status:        Sessão Finalizada")
            print(f"Energia:       {kwh_desejado:.2f} kWh")
            print(f"Tempo Real:    {tempo_minutos:.0f} min")
            print(f"Tarifa Aplicada: R$ {tarifa:.2f} ({tipo})")
            print("-" * 45)
            print(f"TOTAL DEVIDO:  R$ {custo_total:.2f}")
            print("="*45)
            self.log("Pagamento processado via integração ChargeGrid.")

        except ValueError:
            self.log("ERRO: Entrada inválida. Use apenas números.")

    def assistente_conversacional(self):
        """Módulo de atendimento técnico (IA de Contexto)."""
        pergunta = input("\n[Atendimento] Como posso ajudar com o sistema hoje?\n>> ").lower()
        
        # Lógica de triagem de escopo (RF10)
        achou_resposta = False
        for chave, resposta in self.faq.items():
            if chave in pergunta:
                self.log(resposta)
                achou_resposta = True
                break
        
        if not achou_resposta:
            self.log("Essa solicitação está fora do meu escopo técnico. Por favor, acione o suporte avançado GoodWe.")

    def menu(self):
        print(f"\n--- ChargeGrid Intelligence v{self.versao} ---")
        while True:
            print("\n[1] Iniciar Nova Recarga (Cálculo/Pagamento)")
            print("[2] Dúvidas Técnicas (Atendimento GRID)")
            print("[3] Sair")
            
            opcao = input("\nSelecione: ")
            
            if opcao == "1":
                self.processar_pagamento_e_carga()
            elif opcao == "2":
                self.assistente_conversacional()
            elif opcao == "3":
                self.log("Sistema encerrado. Conectando à nuvem...")
                break
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    app = GRIDIntelligenceV3()
    app.menu()