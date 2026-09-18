from model import model_lead
import control

def add_lead():
    name = input("Digite o nome do lead: ")
    email = input("Digite o email do lead: ")
    status = input("Digite o status do lead: ")
    
    # validar dados
    # agora, preciso modelar os dados
    # para isso, vamos usar o módulo model.py
    # preciso modelar os dados como um dicionário
    model_lead(name, email, status)

    # com os dados modelados, preciso enviar para o .json
    # vou usar o control para enviar o dicionário do lead 
    
    print("Lead adicionado, vindo da função")

def main():
    while True:
        print("\nMini CRM de Leads")
        print("1 - Cadastrar Lead")
        print("2 - Listar Leads")
        print("0 - Sair")

        opt = input("Escolha uma opção: ")
        if opt == "1":
            add_lead()
        elif opt == "2":
            print("Listando leads...")
        elif opt == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()