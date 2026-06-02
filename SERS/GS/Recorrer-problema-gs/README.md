# 🌍 Global Solution 2026.1: SERS - Soluções em Energias Renováveis e Sustentáveis

![Python Status](https://img.shields.io/badge/Python-3.x-blue.svg)
![Status](https://img.shields.io/badge/Status-Concluído-success.svg)
![Instituição](https://img.shields.io/badge/Instituição-FIAP-ed145b.svg)
![Curso](https://img.shields.io/badge/Curso-Ciência_da_Computação-black.svg)

## 📋 Sobre o Projeto

Este projeto compõe a entrega acadêmica da Global Solution e tem como foco o monitoramento inteligente de sistemas energéticos para uma missão espacial experimental[cite: 1]. 

Com o avanço da exploração espacial, gerenciar a energia de forma sustentável tornou-se um elemento fundamental para a segurança das missões[cite: 1]. Nossa solução computacional foi desenvolvida para receber, interpretar e exibir dados simulados das condições operacionais dos módulos da missão, aplicando conceitos de energia, potência e sustentabilidade[cite: 1].

## 🎯 Objetivos e Requisitos Atendidos

O sistema foi desenhado para cumprir rigorosamente os requisitos técnicos mínimos do desafio[cite: 1]:

*   **📡 Monitoramento de Dados Simulados:** Captação contínua e autônoma de variáveis como temperatura do módulo, qualidade do sinal de comunicação, percentual de energia nas baterias e captação solar (em kW)[cite: 1].
*   **⚠️ Geração de Alertas:** Sistema automatizado que identifica anomalias e gera alertas imediatos diante de condições críticas simuladas (ex: superaquecimento ou perda de sinal)[cite: 1].
*   **🧠 Tomada de Decisão Básica:** Implementação de estruturas lógicas em código que executam respostas automatizadas para mitigação de riscos (ex: desativar sistemas não essenciais em caso de bateria baixa)[cite: 1].
*   **📊 Visualização dos Dados:** Um painel (dashboard via terminal) que apresenta todas as informações monitoradas e o status operacional de forma clara, organizada e simplificada[cite: 1].

## ⚙️ Arquitetura do Sistema

O projeto foi construído utilizando **Python**, focando em eficiência de código e clareza estrutural[cite: 1]. A arquitetura se divide em três módulos principais executados de forma sequencial:
1.  **Gerador de Telemetria (`simular_telemetria`):** Responsável por injetar dados variáveis no sistema, emulando os sensores do módulo espacial.
2.  **Motor de Decisão (`processar_decisoes_e_alertas`):** O "cérebro" da operação. Analisa os dados em tempo real e define se a operação está ESTÁVEL, em ALERTA ou em estado CRÍTICO, disparando ações corretivas.
3.  **Interface de Visualização (`exibir_painel`):** Renderiza o dashboard atualizado no terminal do usuário.

## 🚀 Como Executar o Projeto

### Pré-requisitos
*   Python 3.x instalado em sua máquina.
*   Terminal de comando (CMD, PowerShell ou terminal integrado de IDEs como VS Code).
*   Nenhuma biblioteca externa de terceiros é necessária (o código utiliza apenas as bibliotecas nativas `random` e `time`).

### Passos para Instalação e Execução

1.  **Clone o repositório:**
```bash
    git clone [https://github.com/lucas-moraca/seu-repositorio-aqui.git](https://github.com/lucas-moraca/seu-repositorio-aqui.git)
    ```
2.  **Navegue até o diretório do projeto:**
```bash
    cd seu-repositorio-aqui
    ```
3.  **Execute a aplicação:**
```bash
    python monitoramento.py
    ```

## 🎥 Demonstração em Vídeo

Como parte dos entregáveis do projeto[cite: 1], elaboramos um vídeo de demonstração abordando o funcionamento da plataforma, a explicação da lógica de tomada de decisão automatizada e os resultados obtidos.

▶️ **[Clique aqui para assistir à demonstração no YouTube](https://youtu.be/SEU_LINK_AQUI)**

## 👨‍💻 Desenvolvedor / Equipe

*   **Lucas Kiodi Moraca** - RM: [Seu RM aqui] - Ciência da Computação
*   [Nome do Integrante 2, se houver] - RM: [RM aqui]
*   [Nome do Integrante 3, se houver] - RM: [RM aqui]

---
*Projeto desenvolvido para fins acadêmicos com foco na integração de algoritmos, pensamento computacional e princípios de inteligência artificial aplicados à indústria aeroespacial[cite: 1].*