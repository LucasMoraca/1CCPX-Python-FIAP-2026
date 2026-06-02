import random
import time

def simular_telemetria():
    """Gera dados simulados do módulo espacial e seus sistemas de energia."""
    return {
        "energia_baterias_pct": round(random.uniform(15.0, 100.0), 2),
        "captacao_solar_kw": round(random.uniform(0.0, 15.5), 2),
        "temperatura_modulo_c": round(random.uniform(-40.0, 95.0), 2),
        "comunicacao_sinal": random.choice(["ONLINE", "ONLINE", "INTERMITENTE", "OFFLINE"]),
        "status_operacional": random.choice(["ESTÁVEL", "ALERTA", "CRÍTICO"])
    }

def processar_decisoes_e_alertas(dados):
    """Aplica a lógica de tomada de decisão baseada nos dados lidos."""
    alertas = []
    
    # Análise de Energia Sustentável (Solar/Baterias)
    if dados["energia_baterias_pct"] < 30.0 and dados["captacao_solar_kw"] < 5.0:
        alertas.append("[CRÍTICO] Energia baixa e captação solar insuficiente. Desativando sistemas não essenciais.")
    elif dados["energia_baterias_pct"] < 40.0:
        alertas.append("[ALERTA] Nível de bateria caindo. Redirecionando matrizes solares para otimização.")
        
    # Análise de Temperatura
    if dados["temperatura_modulo_c"] > 75.0:
        alertas.append("[ALERTA] Superaquecimento detectado. Aumentando potência do sistema de resfriamento.")
    elif dados["temperatura_modulo_c"] < -20.0:
        alertas.append("[ALERTA] Temperatura abaixo do limite. Direcionando energia para suporte de vida e aquecimento.")
        
    # Análise de Comunicação
    if dados["comunicacao_sinal"] == "OFFLINE":
        alertas.append("[CRÍTICO] Perda de sinal com a base. Iniciando protocolo de reconexão de emergência.")

    return alertas

def exibir_painel():
    """Visualização clara e organizada das informações monitoradas."""
    print("\n" + "="*60)
    print("🚀 PAINEL DE MONITORAMENTO: MISSÃO ESPACIAL SUSTENTÁVEL 🚀")
    print("="*60)
    
    dados = simular_telemetria()
    
    print(f"🔋 Nível das Baterias:       {dados['energia_baterias_pct']}%")
    print(f"☀️  Captação Solar Atual:    {dados['captacao_solar_kw']} kW")
    print(f"🌡️  Temperatura do Módulo:   {dados['temperatura_modulo_c']} °C")
    print(f"📡 Status de Comunicação:    {dados['comunicacao_sinal']}")
    print(f"⚙️  Condição Operacional:    {dados['status_operacional']}")
    print("-" * 60)
    
    alertas = processar_decisoes_e_alertas(dados)
    
    if alertas:
        print("⚠️  AÇÕES E ALERTAS DO SISTEMA:")
        for alerta in alertas:
            print(f"   -> {alerta}")
    else:
        print("✅ SISTEMA ESTÁVEL: Operando dentro dos parâmetros sustentáveis normais.")
    print("="*60)

if __name__ == "__main__":
    # Executa a simulação contínua por 3 ciclos como demonstração
    for _ in range(3):
        exibir_painel()
        time.sleep(2)