peca1 = input('Informe o nome da peça: ')
numpeca1 = int(input('Informe a quantidade de peças desejadas: '))
valorpeca1 = float(input('Informe o valor da peça unitária em R$ '))

peca2 = input('Informe o nome da peça: ')
numpeca2 = int(input('Informe a quantidade de peças desejadas: '))
valorpeca2 = float(input('Informe o valor da peça unitária em R$ '))

valorfinalpeca1 = valorpeca1 * numpeca1
valorfinalpeca2 = valorpeca2 * numpeca2

valorfinaldacompra = valorfinalpeca1 + valorfinalpeca2

print('Valor a ser pago com as duas peças: '+ str(valorfinaldacompra))