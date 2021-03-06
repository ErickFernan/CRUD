import socket  # o couchdb faz o uso de socket para conexão
import couchdb


def conectar():
    """
    Função para conectar ao servidor
    """
    user = 'admin'
    password = 'admin'
    conn = couchdb.Server(f'http://{user}:{password}@localhost:5984')

    banco = 'pcouch'

    if banco in conn:  # Se existir esse banco na conexão, a gente o recupera e o retorna
        db = conn[banco]
        return db

    else:  # se não, tenta criar o mesmo
        try:
            db = conn.create(banco)
            return db

        except socket.gaierror as e:
            print(f'Erro ao conectar ao servidor. {e}')
        except couchdb.http.Unauthorized as f:
            print(f'Você não tem permissão de acesso. {f}')
        except ConnectionRefusedError as g:
            print(f'Não foi possível conectar ao servidor. {g}')


def desconectar():
    """ 
    Função para desconectar do servidor.
    """
    print('Desconectando do servidor...')
    # O couchdb faz o desconectar automaticamente


def listar():
    """
    Função para listar os produtos
    """
    db = conectar()

    if db:
        if db.info()['doc_count'] > 0:
            print('Listando produtos...')
            print('--------------------')
            for doc in db:
                print(f"ID: {db[doc]['_id']}")  # O doc é onde se recupera a chave
                print(f"Rev: {db[doc]['_rev']}")  # O doc é onde se recupera a chave
                print(f"Produto: {db[doc]['nome']}")  # O doc é onde se recupera a chave
                print(f"Preço: {db[doc]['preco']}")  # O doc é onde se recupera a chave
                print(f"Estoque: {db[doc]['estoque']}")  # O doc é onde se recupera a chave
                print('--------------------')

        else:
            print('Não existem produtos cadastrados.')
    else:
        print('Não foi possível conectar ao servidor.')


def inserir():
    """
    Função para inserir um produto
    """  
    db = conectar()

    if db:
        nome = input('Informe o nome do produto: ')
        preco = float(input('Informe o preço do produto: '))
        estoque = int(input('Informe o estoque do produto: '))

        produto = {"nome": nome, "preco": preco, "estoque": estoque}

        res = db.save(produto)  # basicamente cria e salva

        if res:
            print(f'O produto {nome} foi inserido com sucesso.')

        else:
            print('O produto não foi salvo.')

    else:
        print('Não foi possível conectar ao servidor.')


def atualizar():
    """
    Função para atualizar um produto
    """
    db = conectar()

    if db:
        chave = input('Informe a chave do produto: ')

        try:
            doc = db[chave]

            nome = input('Informe o nome do produto: ')
            preco = float(input('Informe o preço do produto: '))
            estoque = int(input('Informe o estoque: '))

            doc['nome'] = nome
            doc['preco'] = preco
            doc['estoque'] = estoque

            db[doc.id] = doc
            print(f'O produto {nome} foi atualizado com sucesso.')

        except couchdb.http.ResourceNotFound as e:
            print(f'Produto não encontrado. {e}')

    else:
        print('Não foi possível conectar ao servidor.')


def deletar():
    """
    Função para deletar um produto
    """  
    db = conectar()

    if db:
        _id = input('Informe o ID do produto: ')

        try:
            db.delete(db[_id])
            print('Produto deletado com sucesso.')

        except couchdb.http.ResourceNotFound as e:
            print(f'Produto não encontrado. {e}')

    else:
        print('Não foi possível conectar ao servidor.')


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
