menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar Cliente
[l] Listar Clientes
[u] Criar Conta Corrente
[x] Listar Contas Correntes
[q] Sair

=> """

saldo = 0
extrato = ""
acumula_qtd_saques = 0
limite_vl_saque = 500
LIMITE_QTD_SAQUES = 3
clientes = []
contascorrentes = []

def sacar(*, valor_saque, saldo, extrato, limite_qtd_saques, limite_vl_saque, acumula_qtd_saques):
    
    if valor_saque > 0:      
        if acumula_qtd_saques < limite_qtd_saques:
            if valor_saque <= limite_vl_saque:
                if valor_saque <= saldo:
                    acumula_qtd_saques+=1    
                    saldo -= valor_saque
                    extrato += "- " + str(valor_saque) + "\n"        
                else:
                    print("Saque não permitido. Saldo insuficiente.")
            else:
                print("Saque não permitido. Ultrapassou limite de R$500 por saque.")
        else:
            print("Saque não permitido. Limite diário de 3 saques.")            
    else: 
        print("Só é possível sacar valores positivos.")    
        
    return acumula_qtd_saques, saldo, extrato

def depositar(valor_deposito, saldo, extrato):
    
    if valor_deposito <= 0:
        print("Só é possível depositar valores positivos.")
    else:
        saldo += valor_deposito
        extrato += "+ " + str(valor_deposito) + "\n"
        
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    
    print(extrato + "\n")
    print(f"Saldo Total: R${saldo:.2f}")    
    
    return

def criar_cliente(cpf, nome, data_nascimento, endereco):
    
    novo_cliente = {
        'nome': '',
        'data_nascimento': '',
        'endereco': '',
        'cpf': '' 
    }    
    
    if any(cliente['cpf'] == cpf for cliente in clientes):
        mensagem = f'Cliente com CPF {cpf} já cadastrado'
        return mensagem
    
    novo_cliente = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'endereco': endereco,
        'cpf': cpf      
    }
    
    clientes.append(novo_cliente)
    mensagem = f'Cliente com CPF {cpf} cadastrado com sucesso'
    return mensagem

def listar_clientes():
    
    print('Listagem de Clientes:')
    for contador, cliente in enumerate(clientes, start=1):
        print(f'Cliente #{contador}:')
        print(f'Nome: {cliente["nome"]}')
        print(f'CPF: {cliente["cpf"]}')
        print(f'Data de Nascimento: {cliente["data_nascimento"]}')
        print(f'Endereço: {cliente["endereco"]}\n')


def criar_contacorrente(agencia, numero_cc, cpf_cliente):
        
    nova_contacorrente = {
        'agencia': '',
        'numero' : '',
        'cpf_cliente' : ''
    }
        
    nova_contacorrente = {
        'agencia': agencia,
        'numero' : numero_cc,
        'cpf_cliente' : cpf_cliente        
    }
    
    contascorrentes.append(nova_contacorrente)
    mensagem = f'Conta Corrente {nova_contacorrente['numero']} para o CPF {cpf_cliente} cadastrada com sucesso'
    
    print(mensagem)
    


def listar_contascorrentes():
    
    print('Listagem de Contas Correntes \n')
    
    for cliente in clientes:
        
        contas_do_cliente = [
            conta for conta in contascorrentes if conta['cpf_cliente'] == cliente['cpf']            
        ]
        if not contas_do_cliente:
            continue

        print(f'Cliente: {cliente['nome']}, CPF {cliente['cpf']}:')
        
        for conta in contas_do_cliente:        
            print(f'Agência: {conta['agencia']} - Nº Conta: {conta['numero']}')
        
        print()


while True:

    opcao = input(menu)

    if opcao == "d":
        print("Op. Depósito")
        vl_deposito = float(input("Informe o valor do depósito: "))        
        saldo, extrato = depositar(vl_deposito, saldo, extrato)
                        
    elif opcao == "s":
        print("Op. Saque")
        vl_saque = float(input("Informe o valor do saque: "))        
        acumula_qtd_saques, saldo, extrato = sacar(
            saldo              = saldo,
            valor_saque        = vl_saque,
            extrato            = extrato,
            limite_vl_saque    = limite_vl_saque,
            acumula_qtd_saques = acumula_qtd_saques,
            limite_qtd_saques  = LIMITE_QTD_SAQUES)
        
    elif opcao == "e":
        print("Op. Extrato")
        exibir_extrato(saldo, extrato=extrato)        

    elif opcao == "c":
        print("OP. Criar Cliente")
        print("Informe os dados do novo Cliente:")
        
        cpf             = int(input("Informe o CPF (apenas números): ")) 
        nome            = input("Informe o nome: ")
        data_nascimento = input("Informe a data de nascimento: ")
        endereco        = input("Informe o endereço: ")
        
        print(criar_cliente(cpf, nome, data_nascimento, endereco))
                
    elif opcao == "l":
        print("OP. Listar Clientes")  
        listar_clientes()  

        
    elif opcao == "u":
        print("Op. Criar Conta Corrente")
        cpf_cliente = int(input('Digite o CPF do cliente para quem deseja criar a Conta Corrente: '))

        if any(cliente['cpf'] == cpf_cliente for cliente in clientes):
            print(f'Iniciando processo de cadastro de Conta Corrente para o CPF {cpf_cliente}')
            agencia = '0001'
            
            if len(contascorrentes) == 0:
                proximo_numero = 1
            else:
                proximo_numero = len(contascorrentes) + 1    
                                        
            criar_contacorrente(agencia, proximo_numero, cpf_cliente)
        else:
            print(f'CPF {cpf_cliente} não encontrado na base de Clientes')
            
        
        
    elif opcao == "x":
        print("Op. Listar Contas Correntes")
        listar_contascorrentes()
        
        
    elif opcao == "q":
        print("Sair")
        break
        
    else:
        print("Op. inválida. Selecione novamente a operação desejada.") 