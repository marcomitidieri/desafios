menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        print("Op. Depósito")
        valor = float(input("Informe o valor do depósito: "))
        if valor <= 0:
            print("Só é possível depositar valores positivos.")
        else:
            saldo += valor
            extrato += "+ " + str(valor) + "\n"
                        
    elif opcao == "s":
        print("Op. Saque")
        vl_saque = float(input("Informe o valor do saque: "))
        if vl_saque > 0:      
            if numero_saques < LIMITE_SAQUES:
                if vl_saque <= 500:
                    if vl_saque <= saldo:
                        numero_saques+=1    
                        saldo -= vl_saque
                        extrato += "- " + str(vl_saque) + "\n"        
                    else:
                        print("Saque não permitido. Saldo insuficiente.")
                else:
                    print("Saque não permitido. Ultrapassou limite de R$500 por saque.")
            else:
                print("Saque não permitido. Limite diário de 3 saques.")            
        else: 
            print("Só é possível sacar valores positivos.")

    elif opcao == "e":
        print("Op. Extrato")
        print(extrato + "\n")
        print(f"Saldo Total: R${saldo:.2f}")
        
    elif opcao == "q":
        print("Sair")
        break
        
    else:
        print("Op. inválida. Selecione novamente a operação desejada.") 