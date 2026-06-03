# ⟁ Space Energy Monitor

> **FIAP — Ciência da Computação · Global Solution 2026**  
> Tema: Soluções em Energias Renováveis e Sustentáveis

Sistema inteligente de monitoramento energético para uma missão espacial experimental. Desenvolvido em Python puro, abre automaticamente um **dashboard visual no navegador** com atualização em tempo real via Server-Sent Events (SSE). Dispara alertas automáticos e executa tomadas de decisão autônomas diante de condições críticas — zero dependências externas.

---

## 🎬 Demonstração

> 📺 **Vídeo no YouTube:** `[inserir link]`

---

## 📋 Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Como executar](#como-executar)
- [Parâmetros e limiares](#parâmetros-e-limiares)
- [Tomada de decisão autônoma](#tomada-de-decisão-autônoma)
- [Critérios de avaliação atendidos](#critérios-de-avaliação-atendidos)
- [Integrantes](#integrantes)

---

## Sobre o projeto

O **Space Energy Monitor** simula a central de controle energético de uma missão espacial com quatro módulos operacionais independentes (**Alpha, Beta, Gamma, Delta**). Cada módulo possui sensores virtuais de:

| Métrica | Unidade | Faixa simulada |
|---|---|---|
| Temperatura | °C | 10 – 110 |
| Energia armazenada | % | 0 – 100 |
| Potência consumida | W | 40 – 300 |
| Sinal de comunicação | % | 0 – 100 |
| Captação solar | % | 0 – 100 |

Os dados são atualizados a cada **1,5 segundos** via passeio aleatório suavizado (*drift*), simulando variações reais de ambiente espacial.

---

## Funcionalidades

### 📡 Monitoramento em tempo real
- Dashboard visual no navegador, aberto automaticamente ao executar `python3 monitor.py`
- Atualização contínua via **Server-Sent Events (SSE)** — sem refresh manual
- Barras de progresso coloridas com sparklines SVG de tendência para temperatura, energia e potência
- Banner de alerta global no topo quando qualquer módulo entra em estado crítico ou de alerta
- Resumo global no cabeçalho: energia média, temperatura média, potência total e MET (Mission Elapsed Time)

### 🚨 Geração automática de alertas
Três níveis de alerta, gerados automaticamente ao detectar **transição de status**:

| Nível | Ícone | Condição |
|---|---|---|
| `CRITICO` | ⚠ | Temp ≥ 85 °C **ou** Energia ≤ 15 % **ou** Sinal ≤ 20 % |
| `ALERTA`  | △ | Temp ≥ 70 °C **ou** Energia ≤ 30 % **ou** Sinal ≤ 40 % |
| `INFO`    | ℹ | Módulo retorna ao estado NOMINAL |

Cada alerta registra hora, módulo de origem, mensagem descritiva e ação autônoma executada.

### 🤖 Tomada de decisão autônoma
O sistema aplica um conjunto de regras de decisão em cada ciclo. A resposta é exibida no painel do módulo e registrada no alerta correspondente:

```
Energia ≤ 15%  →  Modo emergência: subsistemas não-essenciais desligados.
Temp   ≥ 85°C  →  Resfriamento emergencial acionado.
Sinal  ≤ 20%   →  Redirecionando para antena de backup.
Energia ≤ 30%  →  Painéis solares adicionais ativados.
Temp   ≥ 70°C  →  Ventilação aumentada para 80%.
```

### 🖥️ Controles interativos
| Botão | Ação |
|---|---|
| `⏸ PAUSAR / ▶ RETOMAR` | Pausa ou retoma a simulação |
| `✕ ALERTAS` | Limpa todos os alertas da central |

Os botões disparam requisições `POST` ao servidor Python, que atualiza o estado e repropaga via SSE para todos os clientes conectados.

---

## Arquitetura

```
space_monitor/
│
├── monitor.py          ← Arquivo principal (único módulo)
│
└── README.md
```

O projeto é **single-file** intencionalmente, para facilitar execução e correção. Internamente o código está organizado em camadas bem separadas:

```
monitor.py
├── Constantes de limiar e configuração
├── Estado global compartilhado (dict thread-safe)
├── Estruturas de dados (dataclasses)
│   ├── DadosModulo
│   └── Alerta
├── Lógica de simulação
│   ├── _drift()           — passeio aleatório suavizado
│   ├── calcular_status()  — classifica NOMINAL / ALERTA / CRITICO
│   └── atualizar_modulo() — aplica variação estocástica
├── Tomada de decisão
│   ├── decisao_autonoma() — regras if/elif em cascata
│   └── gerar_alerta()     — detecta transição de status
├── HTML (string embutida)  — dashboard completo com CSS e JS
├── Servidor HTTP (BaseHTTPRequestHandler)
│   ├── GET  /         — serve o HTML
│   ├── GET  /events   — stream SSE com os dados da simulação
│   ├── POST /pause    — alterna pausado/rodando
│   └── POST /clear    — limpa lista de alertas
├── loop_simulacao()   — thread daemon com o ciclo de atualização
└── __main__           — inicia threads + abre navegador
```

---

## Como executar

### Pré-requisitos
- Python **3.10+**
- Apenas bibliotecas da **stdlib** — `http.server`, `threading`, `webbrowser`, `json`, `dataclasses`
- Nenhum `pip install` necessário, funciona em Windows, macOS e Linux

### Execução

```bash
# Clone o repositório especificando a branch "Java"
git clone -b Java https://github.com/LucasMoraca/1CCPX-Python-FIAP-2026.git

# Navegue até a pasta exata onde o script está localizado
cd 1CCPX-Python-FIAP-2026/SERS/GS

# Execute — o navegador abre automaticamente
python3 monitor2.py
```

O terminal exibirá:
```
  ⟁  SPACE ENERGY MONITOR — FIAP Global Solution 2026
  ──────────────────────────────────────────────────
  Iniciando servidor em http://localhost:8765
  Abrindo dashboard no navegador...
```

Caso o navegador não abra sozinho, acesse manualmente **http://localhost:8765**.  
Para encerrar, pressione `Ctrl+C` no terminal.

---

## Parâmetros e limiares

Todos os limiares estão centralizados no topo de `monitor.py` como constantes, facilitando ajuste:

```python
TEMP_CRITICO    = 85.0   # °C
TEMP_ALERTA     = 70.0   # °C
ENERGIA_CRITICA = 15.0   # %
ENERGIA_ALERTA  = 30.0   # %
SINAL_CRITICO   = 20.0   # %
SINAL_ALERTA    = 40.0   # %
INTERVALO_SEG   = 1.5    # segundos por ciclo
MAX_HISTORICO   = 30     # amostras no sparkline
```

---

## Tomada de decisão autônoma

A função `decisao_autonoma()` implementa uma cadeia de regras `if/elif` que prioriza a condição mais grave:

```python
def decisao_autonoma(mod):
    if mod.energia <= ENERGIA_CRITICA:
        return ">> Modo emergência: subsistemas não-essenciais desligados."
    if mod.temperatura >= TEMP_CRITICO:
        return ">> Resfriamento emergencial acionado."
    if mod.sinal <= SINAL_CRITICO:
        return ">> Redirecionando para antena de backup."
    if mod.energia <= ENERGIA_ALERTA:
        return ">> Painéis solares adicionais ativados."
    if mod.temperatura >= TEMP_ALERTA:
        return ">> Ventilação aumentada para 80%."
    return None
```

Essa lógica é chamada a cada ciclo para exibição no painel e também no momento de geração de alertas críticos.

---
## Integrantes

| Nome completo | RM |
|---|---|
| *Gabriel Barbosa Furin* | *572941* |
| *Lucas Kiodi Moraca* | *571004* |
| *Renan Fracalossi Mano da Silva* | *569610* |

---

> Desenvolvido para a disciplina de **Ciência da Computação — Turmas 1CC**  
> FIAP · Global Solution 2026 · Soluções em Energias Renováveis e Sustentáveis