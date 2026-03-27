nome = input("Informe o nome do colaborador: ")
valordahora = float(input("Valor da hora (R$):"))
horastrabalhadas = float(input("Horas trabalhadas no mês: "))
bonusfixo = float(input("Valor do bônus fixo (R$): "))
descontostotal = float(input("Valor total de descontos (R$): "))

salariobruto = (valordahora * horastrabalhadas) + bonusfixo

salarioliq = salariobruto - descontostotal

print(f"Horas Trabalhadas:      {horastrabalhadas}h")
print(f"Valor da Hora:          R$ {valordahora:.2f}")
print(f"Bônus Mensal:           R$ {bonusfixo:.2f}")
print(f"SALÁRIO BRUTO:          R$ {salariobruto:.2f}")
print(f"Total de Descontos:     R$ {descontostotal:.2f}")
print(f"SALÁRIO LÍQUIDO:        R$ {salarioliq:.2f}")