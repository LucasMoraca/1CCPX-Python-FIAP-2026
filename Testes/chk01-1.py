produto = input("Digite o nome do prouto: ")
valor = float(input("Informe o valor do produo: "))
quantidade = int(input("Informe a quantidade: "))
desconto = float(input("Informe o percentual de desconto (0 - 100): "))

valorbruto = valor * quantidade
valordesconto =  valorbruto * (desconto / 100)
valorfinal = valorbruto - valordesconto

print(f"Produto:           {produto}")
print(f"Qtd:               {quantidade} un.")
print(f"Valor Bruto:       R$ {valorbruto:.2f}")
print(f"Desconto ({desconto}%):  R$ {valordesconto:.2f}")
print(f"TOTAL A PAGAR:     R$ {valorfinal:.2f}")