from datetime import date

dia = int(input('Qual é o seu dia de nascimento?: '))

mes = int(input('Qual mês você nasceu (em número de 1 a 12)?: '))

ano = int(input('Qual é o ano de nascimento? '))

# Pegando a data exata do dia de hoje
hoje = date.today()

# Início dos cálculos
idade = hoje.year - ano
# Verificação: a pessoa já fez aniversário neste ano?
# Se o mês atual for menor que o mês de nascimento, OU
# se estivermos no mesmo mês, mas o dia de hoje for menor que o dia do nascimento...
if hoje.month < mes or (hoje.month == mes and hoje.day < dia):
    idade = idade - 1  # Significa que o aniversário ainda não chegou, então tiramos 1 ano

print(f'Você nasceu em {dia}/{mes}/{ano} e tem {idade} anos.')

#print('Você nasceu em {dia}/{mes}/{ano}'.format(dia=dia, mes=mes, ano=ano))

#outra opção print('Você nasceu em ' + str(dia) + '/' + mes + '/' + str(ano))