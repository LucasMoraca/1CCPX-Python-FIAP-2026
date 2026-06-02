# ⟁ Space Energy Monitor

> **FIAP — Ciência da Computação · Global Solution 2026**  
> Tema: Soluções em Energias Renováveis e Sustentáveis

Sistema inteligente de monitoramento energético para uma missão espacial experimental. Desenvolvido em Python puro, exibe em tempo real os dados simulados dos módulos operacionais da missão, dispara alertas automáticos e executa tomadas de decisão autônomas diante de condições críticas.

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
- Dashboard interativo no terminal com atualização contínua
- Gauge de barra para cada métrica com código de cores dinâmico
- Mini-gráfico de tendência (*sparkline*) para temperatura, energia e potência
- Resumo global: energia média, temperatura média, potência total e captação solar média
- Contador de tempo de missão (MET) e ciclos de simulação

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
| Tecla | Ação |
|---|---|
| `P` | Pausar / Retomar a simulação |
| `L` | Limpar todos os alertas |
| `Q` | Encerrar o programa |

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
├── Constantes de limiar
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
├── Helpers de desenho (curses)
│   ├── barra()            — barra de progresso Unicode
│   └── sparkline()        — gráfico de tendência Unicode
├── Renderização
│   ├── desenhar_cabecalho()
│   ├── desenhar_modulo()
│   ├── desenhar_alertas()
│   └── desenhar_rodape()
└── main() + curses.wrapper()
```

---

## Como executar

### Pré-requisitos
- Python **3.10+**
- Biblioteca `curses` — **já inclusa** na biblioteca padrão do Python (Linux e macOS)

> ⚠️ **Windows:** o módulo `curses` não está disponível nativamente. Use o [Windows Terminal](https://aka.ms/terminal) com WSL2 (Ubuntu) ou instale `windows-curses`:
> ```bash
> pip install windows-curses
> ```

### Execução

```bash
# Clone o repositório
git clone https://github.com/<seu-usuario>/space-energy-monitor.git
cd space-energy-monitor

# Execute diretamente — sem dependências externas
python3 monitor.py
```

O terminal precisa ter pelo menos **100 × 35** caracteres para uma exibição ideal. Use `Ctrl+C` ou pressione `Q` para sair.

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

## Critérios de avaliação atendidos

| Critério | Implementação |
|---|---|
| **Monitoramento de dados simulados** | 5 métricas por módulo, 4 módulos, atualização a cada 1,5 s com drift estocástico |
| **Geração de alertas** | 3 níveis (CRITICO / ALERTA / INFO), disparados automaticamente na transição de status |
| **Tomada de decisão básica** | Função `decisao_autonoma()` com 5 regras priorizadas, resposta exibida em tempo real |
| **Visualização dos dados** | Dashboard curses com barras, sparklines, cores dinâmicas e resumo global |
| **Organização do código** | Separação em camadas (dados → simulação → decisão → renderização), constantes configuráveis |
| **Energias renováveis** | Métrica de captação solar monitorada; ações autônomas priorizam ativação de painéis solares |

---

## Integrantes

| Nome completo | RM |
|---|---|
| *(Adicionar nome)* | *(Adicionar RM)* |
| *(Adicionar nome)* | *(Adicionar RM)* |
| *(Adicionar nome)* | *(Adicionar RM)* |

---

> Desenvolvido para a disciplina de **Ciência da Computação — Turmas 1CC**  
> FIAP · Global Solution 2026 · Soluções em Energias Renováveis e Sustentáveis
