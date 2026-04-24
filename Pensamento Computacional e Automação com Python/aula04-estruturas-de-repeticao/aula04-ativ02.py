def valida_nota(nota):
    while nota < 0 or nota > 10:
        print("A nota deve estar entre 0 e 10")
        nota = float(input("Digite a nota A novamente: "))
    return nota


notaA = float(input("Digite a nota A: "))
notaA = valida_nota(notaA)

notaB = float(input("Digite a nota B: "))
while  notaB < 0 or notaB > 10:
    print("A nota deve estar entre 0 e 10")
    notaA = float(input("Digite a nota B novamente: "))

media = (notaA + notaB) / 2
print(media)