import pyrebase


def conectar():
    """
    Função para conectar ao servidor
    """
    config = {  # documento chave|valor
        "apiKey": "AAAAr-iHNGI:APA91bH3unVGHCWmt7gYoICM0MpzQ1QdU5LCSZRb-vRbAdI7t5PKaVtEIT1ib5tS4B2-HYdpT1UM_e8ak9muyQ1gteczYJ_4DQLH7EUqGMs2kIsacFzIRqPOBbrtz1miiA2NFTSq6fqs",
        "authDomain": "https://crud-fire14-default-rtdb.firebaseio.com/",
        "databaseURL": "https://crud-fire14-default-rtdb.firebaseio.com/",
        "storageBucket": "crud-fire14-default-rtdb.appspot.com"
    }

    conn = pyrebase.initialize_app(config)

    db = conn.database()

    return db


def desconectar():
    """ 
    Função para desconectar do servidor.
    """
    print('Desconectando do servidor...')
    # O firebase fecha a conexão


def listar():
    """
    Função para listar os produtos
    """
    db = conectar()

    produtos = db.child("produtos").get()

    if produtos.val():
        print('Listando produtos...')
        print('--------------------')
        for produto in produtos.each():
            print(f'ID: {produto.key()}')
            print(f"Produto: {produto.val()['nome']}")
            print(f"Preço: {produto.val()['preco']}")
            print(f"Estoque: {produto.val()['estoque']}")
            print('--------------------')

    else:
        print('Não existem produtos cadastrados.')


def inserir():
    """
    Função para inserir um produto
    """  
    db = conectar()

    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe o estoque do produto: '))

    produto = {"nome": nome, "preco": preco, "estoque": estoque}

    res = db.child("produtos").push(produto)

    if 'name' in res:  # O name é a chave retornada
        print(f'O produto {nome} foi cadastrado com sucesso.')
    else:
        print('Não foi possível cadastrar o produto.')


def atualizar():
    """
    Função para atualizar um produto
    """
    db = conectar()

    _id = input('Informe o ID do produto: ')

    produto = db.child('produtos').child(_id).get()  # procura na coleção alguem com o ID = _id

    if produto.val():  # se existe valor, pede os outros produtos
        nome = input('Informe o nome do produto: ')
        preco = float(input('Informe o preço do produto: '))
        estoque = int(input('Informe o estoque do produto: '))

        novo_produto = {"nome": nome, "preco": preco, "estoque": estoque}

        db.child('produtos').child(_id).update(novo_produto)

        print(f'O produto {nome}foi atualizado com sucesso.')

    else:
        print('Não existe produto com o ID informado.')


def deletar():
    """
    Função para deletar um produto
    """  
    db = conectar()

    _id = input('Informe o id do produto: ')

    produto = db.child('produtos').child(_id).get()

    if produto.val():
        db.child('produtos').child(_id).remove()  # este método não retorna valor
        print('O produto foi deletado com sucesso.')
    else:
        print('Não existe produto com o ID informado.')


def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
