# Documento de Requisitos — ChatBot de Atendimento
## ChargeGrid Intelligence

| Campo | Descrição |
| :--- | :--- |
| **Integrantes** | Gabriel Barbosa Furin - RM: 572941; Gabriel de Almeida Santos​ - RM: 569395; Herbert Soares de Jesus​ - RM: 571507; Lucas Kiodi Moraca - RM: 571004; Renan Fracalossi Mano da Silva​ - RM: 569610 |
| **Projeto** | ChatBot de Atendimento — ChargeGrid Intelligence |
| **Parceria** | GoodWe & FIAP |
| **Fase** | Fase 1 — Sprint 1 (S7) |
| **Versão** | 1.0 |
| **Data** | Maio de 2026 |
| **Status** | Entregue |

---

## 1. Introdução e Objetivo da Fase
Este documento formaliza os requisitos levantados na Fase 1 do projeto de desenvolvimento do ChatBot de Atendimento ao Cliente para o ecossistema **ChargeGrid Intelligence**.

> **Objetivo da Fase 1:** Garantir que o escopo do chatbot esteja perfeitamente alinhado com as dores do negócio, definindo o contexto do problema, as lacunas operacionais a serem sanadas e a identidade do assistente virtual.

---

## 2. Análise do Cenário ChargeGrid Intelligence

### 2.1 Contexto do Produto
O **ChargeGrid Intelligence** é a solução de gestão de recarga de veículos elétricos da GoodWe para ambientes comerciais de média e grande escala. O sistema unifica o controle de múltiplos eletropostos em uma única plataforma inteligente.

### 2.2 Problemática Central: Ausência de Mecanismos Integrados
Identificamos quatro dimensões críticas que o sistema resolve e que o chatbot deve abordar:

1.  **Orquestração de Potência:** Evita sobrecarga da rede interna e custos elevados de pico através de balanceamento dinâmico.
2.  **Registro de Ciclos de Recarga:** Garante rastreabilidade, histórico de consumo e relatórios de sustentabilidade.
3.  **Faturamento Automatizado:** Elimina processos manuais e erros de cobrança integrando consumo e financeiro.
4.  **Comunicação do Sistema:** Garante a continuidade através de comunicação redundante e *buffer offline*.

### 2.3 Resumo das Lacunas vs. Abordagem do Chatbot

| Dimensão | Lacuna Sem o Sistema | Como o Chatbot Abordará |
| :--- | :--- | :--- |
| **Orquestração** | Risco de sobrecarga e interrupções | Explicar balanceamento inteligente e limites por ponto |
| **Registro de Ciclos** | Falta de rastreabilidade e histórico | Orientar acesso ao painel e interpretação de dados |
| **Faturamento** | Erros e processos manuais | Esclarecer modelo de cobrança e faturas |
| **Comunicação** | Perda de dados em falhas de rede | Tranquilizar sobre redundância e buffer offline |

---

## 3. Persona e Tom de Voz: GRID

### 3.1 Persona do Chatbot
* **Nome:** GRID
* **Descrição:** Assistente Virtual de Atendimento ChargeGrid Intelligence.
* **Missão:** Orientar usuários e gestores com clareza, precisão técnica e eficiência.

**Atributos de Personalidade:**
* **Técnico e Preciso:** Domínio total do ecossistema.
* **Acessível:** Traduz termos técnicos conforme o perfil.
* **Objetivo:** Respostas diretas e sem rodeios.
* **Profissional:** Tom corporativo B2B.
* **Confiável:** Transmite segurança em cenários de falha.

### 3.2 Diretrizes de Comunicação
* **Linguagem:** Português brasileiro formal, sem gírias ou emojis.
* **Tratamento:** Uso de "você" (equilíbrio entre formal e informal).
* **Escalada:** Direcionar para suporte humano GoodWe quando necessário.

---

## 4. Requisitos Funcionais (RF) — Sprint 1

| ID | Categoria | Descrição do Requisito | Prioridade |
| :--- | :--- | :--- | :--- |
| **RF01** | Orquestração | Responder dúvidas sobre balanceamento de carga. | Alta |
| **RF03** | Registro | Orientar consulta ao histórico de sessões. | Alta |
| **RF05** | Faturamento | Explicar modelo de cobrança e cálculo de consumo. | Alta |
| **RF07** | Comunicação | Informar comportamento em caso de queda de internet. | Alta |
| **RF09** | Persona | Adaptar linguagem ao perfil (motorista vs. gestor). | Alta |

---

## 5. Arquitetura e Seleção Tecnológica

A solução utiliza uma abordagem híbrida para maximizar a eficiência:

1.  **Gemini 1.5 Pro (Google):** Atua como o "cérebro" técnico. Sua alta janela de contexto permite ingerir manuais extensos da GoodWe e suportar futuras análises multimodais (fotos de painéis).
2.  **GPT-4o (OpenAI):** Atua no refinamento da "voz" e raciocínio lógico, garantindo a aderência ao tom de voz corporativo e tratamento de intenções.

### Fluxo de Informação
1.  **Interface:** Captura via Web/App/API.
2.  **Sanitização:** Limpeza de dados e filtro de escopo.
3.  **Injeção de Contexto (RAG):** Consulta aos manuais via LangChain + Definição de Perfil.
4.  **Geração:** Resposta técnica validada e entregue ao usuário.

---

## 6. Cenários Críticos de Avaliação

| ID | Cenário | Pergunta Exemplo | Resposta Ideal |
| :--- | :--- | :--- | :--- |
| **01** | Faturamento | "Como funciona o faturamento?" | Explicar registro em tempo real e faturas automatizadas. |
| **02** | Orquestração | "Carrega vários carros sem cair a luz?" | Confirmar o balanceamento dinâmico inteligente. |
| **04** | Resiliência | "E se a internet cair?" | Informar sobre o armazenamento local (buffer). |

---
> **System Prompt Base:** "Você é o GRID, assistente virtual técnico do sistema ChargeGrid Intelligence da GoodWe. Responda sempre de forma técnica, objetiva e profissional, sem emojis e sem gírias."

 

Documento gerado em Maio de 2026 — GoodWe & FIAP — Sprint 1 (S7) 
