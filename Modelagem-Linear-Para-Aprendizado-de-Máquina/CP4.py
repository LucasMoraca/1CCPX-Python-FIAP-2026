"""
====================================================================
 TEMA: Probabilidade e a Inteligência Artificial
 APLICAÇÃO: Previsão de Risco de Evasão Escolar (área: Educação)
====================================================================

IDEIA CENTRAL DA APRESENTAÇÃO:
A Inteligência Artificial usa Probabilidade para tomar decisões sob
incerteza. Um exemplo clássico é o classificador probabilístico
"Naive Bayes", baseado no Teorema de Bayes:

        P(A|B) = ( P(B|A) * P(A) ) / P(B)

Onde, no nosso problema:
    A = aluno vai evadir (abandonar o curso)
    B = características observadas do aluno (faltas, notas, etc.)

Ou seja: dado que observamos certas características do aluno,
qual é a probabilidade de ele evadir?

Este script tem duas partes:
    PARTE 1 - Um exemplo manual e simples do Teorema de Bayes
              (para explicar o conceito na apresentação).
    PARTE 2 - Uma aplicação real de IA (Naive Bayes) treinada com
              dados de alunos para prever risco de evasão.
====================================================================
"""

import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# Deixa os resultados sempre iguais ao rodar de novo (números pseudoaleatórios)
np.random.seed(42)


# ====================================================================
# PARTE 1 — TEOREMA DE BAYES "NA MÃO" (exemplo didático)
# ====================================================================
print("=" * 70)
print("PARTE 1 - TEOREMA DE BAYES APLICADO A UM CASO SIMPLES")
print("=" * 70)

# Suponha que, historicamente, a escola sabe que:
p_evasao = 0.20          # P(Evasão) -> 20% dos alunos evadem (probabilidade a priori)
p_nao_evasao = 1 - p_evasao

# E que, entre os alunos com MUITAS faltas (mais de 25%):
p_muitas_faltas_dado_evasao = 0.70      # P(Muitas faltas | Evasão)
p_muitas_faltas_dado_nao_evasao = 0.15  # P(Muitas faltas | Não evasão)

# Probabilidade total de um aluno ter muitas faltas (Teorema da Probabilidade Total)
p_muitas_faltas = (p_muitas_faltas_dado_evasao * p_evasao) + \
                   (p_muitas_faltas_dado_nao_evasao * p_nao_evasao)

# Agora aplicamos o Teorema de Bayes:
# Queremos saber: se o aluno TEM muitas faltas, qual a chance dele evadir?
p_evasao_dado_muitas_faltas = (p_muitas_faltas_dado_evasao * p_evasao) / p_muitas_faltas

print(f"P(Evasão) [a priori].................. {p_evasao:.2%}")
print(f"P(Muitas faltas | Evasão)............. {p_muitas_faltas_dado_evasao:.2%}")
print(f"P(Muitas faltas | Não evasão)......... {p_muitas_faltas_dado_nao_evasao:.2%}")
print(f"P(Muitas faltas) [total].............. {p_muitas_faltas:.2%}")
print("-" * 70)
print(f">> P(Evasão | Muitas faltas) = {p_evasao_dado_muitas_faltas:.2%}")
print("Ou seja: saber que o aluno tem muitas faltas FEZ a IA atualizar")
print("a crença sobre o risco de evasão de 20% para "
      f"{p_evasao_dado_muitas_faltas:.0%}.")
print()


# ====================================================================
# PARTE 2 — IA REAL: Naive Bayes prevendo evasão escolar
# ====================================================================
print("=" * 70)
print("PARTE 2 - MODELO DE IA (NAIVE BAYES) PREVENDO EVASÃO ESCOLAR")
print("=" * 70)

# ---- 2.1 Geração de uma base de dados simulada de alunos ----------
# Em uma apresentação real, isso poderia vir de uma planilha da escola.
n_alunos = 300

frequencia = np.random.normal(loc=80, scale=15, size=n_alunos).clip(0, 100)
nota_media = np.random.normal(loc=6.5, scale=1.8, size=n_alunos).clip(0, 10)
horas_estudo_semana = np.random.normal(loc=5, scale=3, size=n_alunos).clip(0, 20)

# Regra "escondida" que gera a evasão real (simula o comportamento do mundo real)
# Quanto menor a frequência e a nota, maior a chance de evasão.
prob_evasao_real = 1 / (1 + np.exp(
    0.08 * (frequencia - 70) + 0.9 * (nota_media - 5) + 0.15 * (horas_estudo_semana - 4)
))
evasao = (np.random.rand(n_alunos) < prob_evasao_real).astype(int)  # 1 = evadiu, 0 = não

dados = pd.DataFrame({
    "frequencia_%": frequencia.round(1),
    "nota_media": nota_media.round(1),
    "horas_estudo_semana": horas_estudo_semana.round(1),
    "evadiu": evasao
})

print("\nAmostra da base de dados simulada:")
print(dados.head(8).to_string(index=False))
print(f"\nTotal de alunos: {n_alunos}")
print(f"Taxa real de evasão na base: {dados['evadiu'].mean():.1%}")

# ---- 2.2 Separando treino e teste ----------------------------------
X = dados[["frequencia_%", "nota_media", "horas_estudo_semana"]]
y = dados["evadiu"]

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ---- 2.3 Treinando o modelo probabilístico (Naive Bayes) ----------
modelo = GaussianNB()
modelo.fit(X_treino, y_treino)

# ---- 2.4 Avaliando o modelo ----------------------------------------
y_previsto = modelo.predict(X_teste)
acuracia = accuracy_score(y_teste, y_previsto)

print("\n" + "-" * 70)
print(f"Acurácia do modelo no conjunto de teste: {acuracia:.1%}")
print("Matriz de confusão (linhas=real, colunas=previsto):")
print(confusion_matrix(y_teste, y_previsto))

# ---- 2.5 Usando a IA para prever o risco de alunos novos -----------
print("\n" + "-" * 70)
print("PREVISÃO DE RISCO PARA NOVOS ALUNOS (o que a IA 'aprendeu')")
print("-" * 70)

novos_alunos = pd.DataFrame({
    "frequencia_%": [95, 60, 40],
    "nota_media":   [8.5, 5.5, 3.0],
    "horas_estudo_semana": [8, 3, 1],
})

probabilidades = modelo.predict_proba(novos_alunos)  # [:,1] = prob. de evadir

for i in range(len(novos_alunos)):
    linha = novos_alunos.iloc[i]
    prob_evadir = probabilidades[i][1]
    if prob_evadir < 0.3:
        risco = "BAIXO"
    elif prob_evadir < 0.6:
        risco = "MÉDIO"
    else:
        risco = "ALTO"
    print(f"Aluno {i+1}: frequência={linha['frequencia_%']:.0f}%, "
          f"nota={linha['nota_media']:.1f}, "
          f"horas_estudo={linha['horas_estudo_semana']:.0f}h/semana "
          f"-> P(evasão) = {prob_evadir:.1%}  [Risco {risco}]")

print("\n" + "=" * 70)
print("CONCLUSÃO PARA A APRESENTAÇÃO:")
print("A IA não 'decide' com certeza absoluta — ela calcula a")
print("PROBABILIDADE de cada evento (evasão ou não) com base em dados")
print("passados, usando o Teorema de Bayes por trás dos panos. Isso")
print("permite priorizar quais alunos a escola deve apoiar primeiro.")
print("=" * 70)