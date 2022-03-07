import redis


def testa_chave(chave):
    try:
        conn = conectar()
        dados = conn.keys(pattern='produtos:*')  # chamar as chaves e depois os produtos
        dados = str(dados)

        if chave in dados:
            return True
        else:
            return False

    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível testar a chave. {e}')


def gera_id():
    try:
        conn = conectar()  # conecta

        chave = conn.get('chave')  # pega a ultima chave, comando get

        if chave:
            chave = conn.incr('chave')  # se a chave existir usa o comando incr do redis para incrementar
            return chave
        else:
            conn.set('chave', 1)  # caso a chave não exista cadastra a primeira
            return 1

    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível gerar a chave. {e}')


def conectar():
    """
    Função para conectar ao servidor
    """
    conn = redis.Redis(host='localhost', port=6379)

    return conn  # É preciso habilitar a conexão


def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    conn.connection_pool.disconnect()


def listar():
    """
    Função para listar os produtos
    """
    conn = conectar()

    try:
        dados = conn.keys(pattern='produtos:*')  # chamar as chaves e depois os produtos

        if len(dados) > 0:
            print('Listando produtos...')
            print('--------------------')

            for chave in dados:
                produto = conn.hgetall(chave)
                print(f"ID: {str(chave,'utf-8', 'ignore')}")
                print(f"Produto: {str(produto[b'nome'],'utf-8', 'ignore')}")
                print(f"Preço: {str(produto[b'preco'],'utf-8', 'ignore')}")
                print(f"Estoque: {str(produto[b'estoque'],'utf-8', 'ignore')}")
                print('--------------------')

                #  Os dados vem em formato de string binária (por isso o b'variável'), por isso converte-se o dado em
                #  utf-8, o ignore é pra ignorar erros que podem aparecer

        else:
            print('Não existem produtos cadastrados.')

    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível listar os produtos. {e}')

    desconectar(conn)


def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()

    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço: '))
    estoque = int(input('Informe o estoque: '))

    produto = {"nome": nome, "preco": preco, "estoque": estoque}  # Chave | valor
    #   padrão seguido será produtos:cod(1,2,3...))
    chave = f'produtos:{gera_id()}'

    try:
        res = conn.hmset(chave, produto)  # lembrando hm pois são multiplos valores

        if res:
            print(f'O produto {nome} foi inserido com suscesso.')
        else:
            print('Não foi possível inserir o produto.')

    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível inserir o produto. {e}')

    desconectar(conn)


def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()

    chave = input('Informe a chave do produto: ')
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço: '))
    estoque = int(input('Informe o estoque: '))

    produto = {"nome": nome, "preco": preco, "estoque": estoque}  # Chave | valor

    resposta = testa_chave(chave)

    if resposta:
        try:
            res = conn.hmset(chave, produto)

            if res:
                print(f'O produto {nome} foi atuaizado com sucesso.')

            # Nesse caso se a chave não existir ela sera criada, então não tem motivo para colocar o else, depois
            # adiciono uma função para não permitir isso, note que no momento a diferenã pro inserir é que a chave é
            # gerada e aqui é recebida

            # O programa foi atualizado, agora possui um fç que trata a chave, se ela existir da continuidade ao código
            # se não interrompe, portanto nã precisa do else

        except redis.exceptions.ConnectionError as e:
            print(f'Não foi possível atualizar o produto. {e}')

    else:
        print('Chave inexistente, confira a escrita.')

    desconectar(conn)


def deletar():
    """
    Função para deletar um produto
    """  
    conn = conectar()

    chave = input('Informe a chave do produto: ')

    try:
        res = conn.delete(chave)

        if res == 1:
            print('O produto foi deletado com sucesso.')
        else:
            print('Não existe produto com a chave informada.')

    except redis.exceptions.ConnectionError as e:
        print(f'Erro ao conectar ao redis. {e}')

    desconectar(conn)


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
