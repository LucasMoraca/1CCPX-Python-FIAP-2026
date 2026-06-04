# 🚀 Mission Control AI

**Integrantes:**
- Gabriel Barbosa Furin - RM: 572941
- Lucas Kiodi Moraca - RM: 571004
- Renan Fracalossi Mano da Silva​ - RM: 569610

---

## 📌 O que o projeto faz

Sistema de monitoramento de missão espacial desenvolvido em Python com IA generativa. Utiliza o modelo **Llama 3.2:1b via Ollama** para analisar dados simulados de temperatura, energia e comunicação em tempo real, gerando alertas automáticos e respostas inteligentes quando a missão entra em situação crítica.

---

## 🎯 Funcionalidades

- ✅ Geração de dados simulados da missão (temperatura, energia, sinal, status dos módulos)
- ✅ Monitoramento de **5 módulos operacionais** (Orbital, Propulsão, Vida, Comunicação, Energia)
- ✅ Alertas automáticos quando parâmetros saem dos limites operacionais
- ✅ Lógica de tomada de decisão (ex: energia < 20% → ativa modo economia)
- ✅ Respostas automatizadas para situações críticas simuladas
- ✅ **IA integrada (ARIA)** que analisa os dados e gera recomendações contextualizadas
- ✅ Dashboard visual no terminal com indicadores coloridos (🟢 🟡 🔴)
- ✅ Monitoramento contínuo com múltiplos ciclos

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| Ollama | Servidor local do modelo de linguagem |
| Llama 3.2:1b | Modelo de IA para análise da missão |
| Google Colab | Ambiente de execução |
| `random`, `datetime`, `time` | Geração de dados simulados e controle de tempo |

---

## 🖼️ Demonstração

### Cenário Normal — missão operando dentro dos parâmetros

![Dados normais da missão](Captura%20de%20tela%202026-06-04%20134205.png)

### Cenário Crítico — alertas ativos e resposta da IA

![Alerta crítico com análise da IA](Captura%20de%20tela%202026-06-04%20134250.png)

---

## ▶️ Como Executar

Abra o notebook diretamente no Google Colab:

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1dtScFWjjL0W5yXVCh1uwgrUMHh_64mVA?usp=sharing)


### Passo a passo:

1. Acesse o link do Colab acima
2. Execute as células **em ordem**, de cima para baixo
3. A célula de instalação (Passo 1) pode levar alguns minutos — aguarde
4. O modelo Llama será instalado automaticamente via Ollama
5. Execute o **Passo 7A** para ver o cenário normal
6. Execute o **Passo 7B** para ver o cenário crítico com alertas
7. Execute o **Passo 8** para o monitoramento contínuo com 3 ciclos

> 💡 Não é necessário criar conta, chave de API ou instalar nada localmente.

---

## 🎬 Vídeo de Demonstração

[▶️ Assistir ao vídeo](https://youtu.be/4GFWJ7Yf5N4)


---

## 📊 Limites Operacionais da Missão

| Parâmetro | Mínimo | Máximo | Ação em caso crítico |
|---|---|---|---|
| Temperatura | -20°C | 85°C | Ativa resfriamento emergencial |
| Energia | 20% | 100% | Ativa modo economia |
| Sinal | 40% | 100% | Aciona antena secundária |

---

## 🏗️ Estrutura do Projeto

```
mission-control-ai/
├── mission_control_ai.ipynb   # Notebook principal
├── README.md                  # Este arquivo
└── assets/                    # Prints do sistema rodando
    ├── dados_normais.png
    ├── alerta_critico.png
    ├── monitoramento_continuo.png
    └── analise_ia.png
```

---

*FIAP — Global Solution 2026.1 | Prompt and Artificial Intelligence | Prof. José Maia Neto*
