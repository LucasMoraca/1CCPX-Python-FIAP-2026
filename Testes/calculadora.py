def calculadora():
    """
    Executa uma calculadora interativa via terminal.

    O programa exibe um menu, recebe a opção do usuário e realiza as quatro
    operações matemáticas básicas (soma, subtração, multiplicação e divisão),
    além de tratar erros de entrada e divisão por zero.
    """
    while True:
        # Exibição visual do menu de opções
        print("\n" + "=" * 25)
        print("   MENU DA CALCULADORA")
        print("=" * 25)
        print("1. Soma (+)")
        print("2. Subtração (-)")
        print("3. Multiplicação (*)")
        print("4. Divisão (/)")
        print("0. Sair")
        print("=" * 25)

        # Recebe a escolha do usuário e limpa espaços extras com .strip()
        opcao = input("Escolha uma opção: ").strip()

        # Condição de saída: encerra o laço while
        if opcao == '0':
            print("\nEncerrando... Até a próxima!")
            break

        # Validação: garante que a opção esteja na lista de strings permitidas
        if opcao not in ['1', '2', '3', '4']:
            print("\n[!] OPÇÃO INVÁLIDA! Por favor, escolha de 0 a 4.")
            continue

        try:
            # Converte as entradas de texto para números decimais (float)
            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))

            print("-" * 25)

            # Estrutura de decisão para escolher a operação matemática
            if opcao == '1':
                print(f"Resultado: {num1} + {num2} = {num1 + num2}")

            elif opcao == '2':
                print(f"Resultado: {num1} - {num2} = {num1 - num2}")

            elif opcao == '3':
                print(f"Resultado: {num1} * {num2} = {num1 * num2}")

            elif opcao == '4':
                # Verificação lógica para evitar erro matemático de divisão por zero
                if num2 != 0:
                    print(f"Resultado: {num1} / {num2} = {num1 / num2}")
                else:
                    print("Erro: Não é possível dividir por zero!")

            print("-" * 25)

        except ValueError:
            # Captura erros de conversão (ex: quando o usuário digita letras)
            print("\n[!] ERRO: Você deve digitar números válidos (ex: 10 ou 5.5).")


# Ponto de entrada padrão do script Python
if __name__ == "__main__":
    calculadora()