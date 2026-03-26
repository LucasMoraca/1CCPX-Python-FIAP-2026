# Recebendo os valores digitados
valor_produto = float(input('Digite o valor do produto (R$): '))
valor_pago = float(input('Digite o valor pago pelo cliente (R$): '))

# Calculando o troco (valor pago menos o valor do produto)
troco = valor_pago - valor_produto

# Exibindo o resultado
# O ":.2f" garante que o número terá exatamente 2 casas após a vírgula/ponto
print(f'O troco a ser pago é de R$ {troco:.2f}')