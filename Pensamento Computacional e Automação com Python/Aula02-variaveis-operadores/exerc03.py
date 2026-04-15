# Recebendo os valores do usuário (usamos float para permitir números quebrados)
distancia = float(input('Qual é a distância percorrida (em km)?: '))
velocidade = float(input('Qual foi a velocidade média (em km/h)?: '))

# Verificando se a velocidade não é zero para evitar erro de divisão
if velocidade <= 0:
    print('A velocidade deve ser maior que zero!')
else:
    # Calculando o tempo
    tempo = distancia / velocidade

    # Mostrando o resultado
    print(f'O tempo estimado de viagem é de {tempo} horas.')