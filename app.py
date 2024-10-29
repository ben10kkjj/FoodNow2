import json

from flask import Flask, request, Response
from sqlalchemy import select

from models import *
app = Flask(__name__)


@app.route('/add_produto', methods=['POST'])
def add_produto():
    #
    # Criando o produto
    produto = Produto(
        nome_produto=request.form['nome_produto'],
        preco_produto=float(request.form['preco_produto']),
        disponivel=int(request.form['disponivel']),
        id_categoria=int(request.form['id_categoria']),
        id_cardapio=int(request.form['id_Cardapio'])
    )
    print(produto)
    # Salvando o produto no banco
    produto.save()

    # Resposta em JSON
    final = {
        'status': 'success',
        'id_produto': produto.id_produto,
        'nome_produto': produto.nome_produto,
        'preco_produto': produto.preco_produto,
        'disponivel': produto.disponivel,
        'id_categoria': produto.id_categoria,
        'id_cardapio': produto.id_cardapio,
    }

    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )
    # except Exception as e:
    #     # Outro erro genérico
    #     return jsonify({'error': f'Erro ao adicionar o produto'}), 500


@app.route('/get_produtos', methods=['GET'])
def consultar_produtos():
    produto = Produto.query.all()
    result = []
    for consulta in produto:
        result.append(consulta.serialize_produto())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/get_produto/<id>', methods=['GET'])
def consultar_produto(id):
    produto_sql = select(Produto).where(Produto.id_produto == id)
    produto = db_session.execute(produto_sql).scalar()
    final = {
        'status': 'success',
        'id': produto.id_produto,
        'nome_produto': produto.nome_produto,
        'preco_produto': produto.preco_produto,
        'disponivel': produto.disponivel,
        'id_Categoria': produto.id_categoria,
        'id_Cardapio': produto.id_cardapio
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json'
                    )


@app.route('/updateProduto/<id>', methods=['PUT'])
def update(id):
    produto = select(Produto).where(Produto.id_produto == id)
    produto = db_session.execute(produto).scalar()
    produto.nome = request.form['nome_produto']
    produto.preco_produto = float(request.form['preco_produto'])
    produto.disponivel = int(request.form['disponivel'])
    produto.id_Categoria = int(request.form['id_Categoria'])
    produto.id_Cardapio = int(request.form['id_Cardapio'])
    db_session.commit()
    final = {
        'status': 'success',
        'id': produto.id_produto,
        'nome_produto': produto.nome_produto,
        'preco_produto': produto.preco_produto,
        'disponivel': produto.disponivel,
        'id_Categoria': produto.id_Categoria,
        'id_Cardapio': produto.id_Cardapio
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/deleteProduto/<id>', methods=['DELETE'])
def delete(id):
    produto = select(Produto).where(Produto.id_produto == id)
    produto = db_session.execute(produto).scalar()
    final = {
        'status': 'removido',
        'id': produto.id_produto,
        'nome': produto.nome_produto,
        'preco': produto.preco_produto,
        'disponivel': produto.disponivel
    }

    produto.delete()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addCategoria', methods=['POST'])
def add_categoria():
    form_evento = Categoria(nome_Categoria=request.form['nome_Categoria'])
    print(form_evento)
    form_evento.save()
    # db_session.close()

    final = {
        'status': 'success',
        'id_Categoria': form_evento.id_categoria,
        'nome_Categoria': form_evento.nome_Categoria,
    }
    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json')


@app.route('/getCategorias', methods=['GET'])
def get_categorias():
    categoria = Categoria.query.all()
    result = []
    for consulta in categoria:
        result.append(consulta.serialize_categoria())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/updateCategoria/<id>', methods=['PUT'])
def update_categoria(id):
    categoria = select(Categoria).where(Categoria.id_categoria == id)
    categoria = db_session.execute(categoria).scalar()
    categoria.nome_Categoria = request.form['nome_Categoria']
    db_session.commit()
    final = {
        'status': 'atualizado',
        'id': categoria.id_categoria,
        'nome_Categoria': categoria.nome_Categoria
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/deleteCategoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    categoria = select(Categoria).where(Categoria.id_categoria == id)
    categoria = db_session.execute(categoria).scalar()
    final = {
        'status': 'removido',
        'id': categoria.id_categoria,
        'nome': categoria.nome_Categoria}
    db_session.delete(categoria)
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addCliente', methods=['POST'])
def add_cliente():
    cliente = Cliente(
        nome_cliente=request.form['nome_cliente'],
        senha_cliente=request.form['senha_cliente'],
        email_cliente=request.form['email_cliente'],
        telefone_cliente=int(request.form['telefone_cliente']),
        endereco_cliente=request.form['endereco_cliente']
    )

    print(cliente)
    # Salvando o produto no banco
    db_session.add(cliente)
    cliente.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': cliente.id_cliente,
        'nome_cliente': cliente.nome_cliente,
        'senha_cliente': cliente.senha_cliente,
        'email_cliente': cliente.email_cliente,
        'telefone_cliente': cliente.telefone_cliente,
        'endereco_cliente': cliente.endereco_cliente
    }

    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getCliente', methods=['GET'])
def get_cliente():
    cliente = Cliente.query.all()
    result = []
    for consulta in cliente:
        result.append(consulta.serialize_cliente())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/updateCliente/<id>', methods=['PUT'])
def update_cliente(id):
    cliente = select(Cliente).where(Cliente.id_cliente == id)
    cliente = db_session.execute(cliente).scalar()
    cliente.nome = request.form['nome_cliente']
    cliente.senha = int(request.form['senha_cliente'])
    cliente.email = request.form['email_cliente']
    cliente.telefone = int(request.form['telefone_cliente'])
    cliente.endereco = request.form['endereco_cliente']
    db_session.commit()
    final = {
        'status': 'success',
        'id': cliente.id_cliente,
        'nome_cliente': cliente.nome_cliente,
        'senha_cliente': cliente.senha_cliente,
        'email_cliente': cliente.email_cliente,
        'telefone_cliente': cliente.telefone_cliente,
        'endereco_cliente': cliente.endereco_cliente
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/deleteCliente/<id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = select(Cliente).where(Cliente.id_cliente == id)
    cliente = db_session.execute(cliente).scalar()
    final = {
        'status': 'removido',
        'id': cliente.id_cliente,
        'nome_cliente': cliente.nome_cliente,
        'senha_cliente': cliente.senha_cliente,
        'email_cliente': cliente.email_cliente,
        'telefone_cliente': cliente.telefone_cliente,
        'endereco_cliente': cliente.endereco_cliente
    }
    db_session.delete(cliente)
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addCardapio', methods=['POST'])
def add_cardapio():
    cardapio = Cardapio(
        nome_cardapio=request.form['nome_cardapio'],
        descricao_cardapio=request.form['descricao_cardapio']
    )
    print(cardapio)
    # Salvando o produto no banco
    db_session.add(cardapio)
    cardapio.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': cardapio.id_cardapio,
        'nome_cardapio': cardapio.nome_cardapio,
        'descricao_cardapio': cardapio.descricao_cardapio
    }

    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getCardapio', methods=['GET'])
def get_cardapio():
    cardapio = Cardapio.query.all()
    result = []
    for consulta in cardapio:
        result.append(consulta.serialize_cardapio())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/updateCardapio/<id>', methods=['PUT'])
def update_cardapio(id):
    cardapio = select(Cardapio).where(Cardapio.id_cardapio == id)
    cardapio = db_session.execute(cardapio).scalar()
    cardapio.nome = request.form['nome_cardapio']
    cardapio.descricao = request.form['descricao_cardapio']
    db_session.commit()
    final = {
        'status': 'success',
        'id': cardapio.id_cardapio,
        'nome_cardapio': cardapio.nome_cardapio,
        'descricao_cardapio': cardapio.descricao_cardapio
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/deleteCardapio/<id>', methods=['DELETE'])
def delete_cardapio(id):
    cardapio = select(Cardapio).where(Cardapio.id_cardapio == id)
    cardapio = db_session.execute(cardapio).scalar()
    final = {
        'status': 'removido',
        'id': cardapio.id_cardapio,
        'nome_cardapio': cardapio.nome_cardapio,
        'descricao_cardapio': cardapio.descricao_cardapio}
    db_session.delete(cardapio)
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addCarrinho', methods=['POST'])
def add_carrrinho():
    carrinho = Carrinho(
        data_pedido=request.form['data_pedido'],
        quantidade=int(request.form['quantidade']),
        id_cliente=int(request.form['id_cliente']),
        id_produto=int(request.form['id_produto']),
        tempo_producao=request.form['tempo_producao'],
        preco_total=float(request.form['preco_total'])
    )
    print(carrinho)
    # Salvando o produto no banco
    db_session.add(carrinho)
    carrinho.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': carrinho.id_carrinho,
        'data_pedido': carrinho.data_pedido,
        'quantidade': carrinho.quantidade,
        'id_cliente': carrinho.id_cliente,
        'id_produto': carrinho.id_produto,
        'tempo_producao': carrinho.tempo_producao,
        'preco_total': carrinho.preco_total
    }

    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getCarrinho/<id>', methods=['GET'])
def get_carrrinho(id):
    carrinho = Carrinho.query.all()
    result = []
    for consulta in carrinho:
        result.append(consulta.serialize_carrinho())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/updateCarrinho/<id>', methods=['PUT'])
def update_carrrinho(id):
    carrinho = select(Carrinho).where(Carrinho.id_carrinho == id)
    carrinho = db_session.execute(carrinho).scalar()
    carrinho.data_pedido = request.form['data_pedido']
    carrinho.quantidade = int(request.form['quantidade'])
    carrinho.id_cliente = int(request.form['id_cliente'])
    carrinho.id_produto = int(request.form['id_produto'])
    carrinho.tempo_producao = request.form['tempo_producao']
    carrinho.preco_total = request.form['preco_total']
    db_session.commit()
    final = {
        'status': 'success',
        'id': carrinho.id_carrinho,
        'data_pedido': carrinho.data_pedido,
        'quantidade': carrinho.quantidade,
        'id_cliente': carrinho.id_cliente,
        'id_produto': carrinho.id_produto,
        'tempo_producao': carrinho.tempo_producao,
        'preco_total': carrinho.preco_total
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/deleteCarrinho/<id>', methods=['DELETE'])
def delete_carrrinho(id):
    carrinho = select(Carrinho).where(Carrinho.id_carrinho == id)
    carrinho = db_session.execute(carrinho).scalar()
    final = {
        'status': 'removido',
        'id': carrinho.id_carrinho,
        'data_pedido': carrinho.data_pedido,
        'quantidade': carrinho.quantidade,
        'id_cliente': carrinho.id_cliente,
        'id_produto': carrinho.id_produto,
        'tempo_producao': carrinho.tempo_producao,
        'preco_total': carrinho.preco_total}
    db_session.delete(carrinho)
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addEmpresa', methods=['POST'])
def add_empresa():
    empresa = Empresa(
        nome_empresa=request.form['nome_empresa'],
        endereco_empresa=request.form['endereco_empresa'],
        id_cardapio=int(request.form['id_cardapio']),
        cnpj_empresa=int(request.form['cnpj_empresa']),
        email_empresa=request.form['email_empresa'],
        senha_empresa=request.form['senha_empresa']
    )
    print(empresa)
    # Salvando o produto no banco
    db_session.add(empresa)
    empresa.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': empresa.id_empresa,
        'nome_empresa': empresa.nome_empresa,
        'endereco_empresa': empresa.endereco_empresa,
        'id_cardapio': empresa.id_cardapio,
        'cnpj_empresa': empresa.cnpj_empresa,
        'senha_empresa': empresa.senha_empresa,
        'email_empresa': empresa.email_empresa
    }

    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getEmpresa', methods=['GET'])
def get_empresa():
    empresa = Empresa.query.all()
    result = []
    for consulta in empresa:
        result.append(consulta.serialize_empresa())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')

@app.route('/get_empresa/<id>', methods=['GET'])
def consultar_empresa_id(id):
    empresa_sql = select(Empresa).where(Empresa.id_empresa == id)
    empresa = db_session.execute(empresa_sql).scalar()
    final = {
        'status': 'success',
        'id': empresa.id_empresa,
        'nome_empresa': empresa.nome_empresa,
        'endereco_empresa': empresa.endereco_empresa,
        'cnpj_empresa': empresa.cnpj_empresa,
        'email_empresa': empresa.email_empresa,
        'senha_empresa': empresa.senha_empresa
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json'
                    )

@app.route('/get_empresa_cnpj/<cnpj>', methods=['GET'])
def consultar_empresa_cnpj(cnpj):
    empresa_sql = select(Empresa).where(Empresa.cnpj_empresa == cnpj)
    empresa = db_session.execute(empresa_sql).scalar()
    if empresa is None:
        final = {
            'status': 'success',
            'msg_erro': 'Essa empresa não existe'
        }
    else:
        final = {
            'status': 'success',
            'cnpj': empresa.cnpj_empresa,
            'nome_empresa': empresa.nome_empresa,
            'endereco_empresa': empresa.endereco_empresa,
            'email_empresa': empresa.email_empresa,
            'senha_empresa': empresa.senha_empresa
        }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json'
                    )


@app.route('/updateEmpresa/<id>', methods=['PUT'])
def update_empresa(id):
    empresa = select(Empresa).where(Empresa.id_empresa == id)
    empresa = db_session.execute(empresa).scalar()
    empresa.nome_empresa = request.form['nome_empresa']
    empresa.endereco_empresa = request.form['endereco_empresa']
    empresa.id_cardapio = int(request.form['id_cardapio'])
    cnpj_empresa = int(request.form['cnpj_empresa'])
    email_empresa = request.form['email_empresa']
    senha_empresa = request.form['senha_empresa']
    db_session.commit()
    final = {
        'status': 'success',
        'id': empresa.id_empresa,
        'nome_empresa': empresa.nome_empresa,
        'endereco_empresa': empresa.endereco_empresa,
        'id_cardapio': empresa.id_cardapio,
        'cnpj_empresa': empresa.cnpj_empresa,
        'email_empresa': empresa.email,
        'senha_empresa': empresa.senha_empresa
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/deleteEmpresa/<id>', methods=['DELETE'])
def delete_empresa(id):
    empresa = select(Empresa).where(Empresa.id_empresa == id)
    empresa = db_session.execute(empresa).scalar()
    final = {
        'status': 'removido',
        'id': empresa.id_empresa,
        'nome_empresa': empresa.nome_empresa,
        'endereco_empresa': empresa.endereco_empresa,
        'id_cardapio': empresa.id_cardapio,
        'cnpj_empresa': empresa.cnpj_empresa,
        'email_empresa': empresa.email_empresa,
        'senha_empresa': empresa.senha_empresa
    }
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addIngrediente', methods=['POST'])
def add_ingrediente():
    ingrediente = Ingrediente(
        nome_ingrediente=request.form['nome_ingrediente'],
    )
    print(ingrediente)
    # Salvando o produto no banco
    db_session.add(ingrediente)
    ingrediente.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': ingrediente.id_ingrediente,
        'nome_ingrediente': ingrediente.nome_ingrediente,
    }
    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getIngrediente', methods=['GET'])
def get_ingrediente():
    ingrediente = Ingrediente.query.all()
    result = []
    for consulta in ingrediente:
        result.append(consulta.serialize_ingrediente())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/updateIngrediente/<id>', methods=['PUT'])
def update_ingrediente(id):
    ingrediente = select(Ingrediente).where(Ingrediente.id_ingrediente == id)
    ingrediente = db_session.execute(ingrediente).scalar()
    ingrediente.nome_ingrediente = request.form['nome_ingrediente']
    db_session.commit()
    final = {
        'status': 'success',
        'id': ingrediente.id_ingrediente,
        'nome_ingrediente': ingrediente.nome_ingrediente
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/deleteIngrediente/<id>', methods=['DELETE'])
def delete_ingrediente(id):
    ingrediente = select(Ingrediente).where(Ingrediente.id_ingrediente == id)
    ingrediente = db_session.execute(ingrediente).scalar()
    final = {
        'status': 'removido',
        'id': ingrediente.id_ingrediente,
        'nome_ingediente': ingrediente.nome_ingrediente
    }
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addIngrediente_produto', methods=['POST'])
def add_ingrediente_produto():
    ingrediente_produto = Ingrediente_produto(
        id_produto=int(request.form['id_produto']),
        id_ingrediente=int(request.form['id_ingrediente']),
    )
    print(ingrediente_produto)
    # Salvando o produto no banco
    db_session.add(ingrediente_produto)
    ingrediente_produto.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': ingrediente_produto.id_ingrediente_produto,
        'id_ingrediente': ingrediente_produto.id_ingrediente,
        'id_produto': ingrediente_produto.id_produto
    }
    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getIngrediente_produto', methods=['GET'])
def get_ingrediente_produto():
    ingrediente_produto = Ingrediente_produto.query.all()
    result = []
    for consulta in ingrediente_produto:
        result.append(consulta.serialize_ingrediente_produto())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/updateIngrediente_produto/<id>', methods=['PUT'])
def update_ingrediente_produto(id):
    ingrediente_produto = select(Ingrediente_produto).where(Ingrediente_produto.id_ingrediente_produto == id)
    ingrediente_produto = db_session.execute(ingrediente_produto).scalar()
    db_session.commit()
    final = {
        'status': 'atualizado',
        'id': ingrediente_produto.id_ingrediente_produto,
        'id_ingrediente': ingrediente_produto.id_ingrediente,
        'id_produto': ingrediente_produto.id_produto
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/deleteIngrediente_produto/<id>', methods=['DELETE'])
def delete_ingrediente_produto(id):
    ingrediente_produto = select(Ingrediente_produto).where(Ingrediente_produto.id_ingrediente_produto == id)
    ingrediente_produto = db_session.execute(ingrediente_produto).scalar()
    final = {
        'status': 'removido',
        'id': ingrediente_produto.id_ingrediente_produto,
        'id_ingrediente': ingrediente_produto.id_ingrediente,
        'id_produto': ingrediente_produto.id_produto
    }
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addFavorito', methods=['POST'])
def add_favorite():
    favorito = Favorito(
        id_cliente=int(request.form['id_cliente']),
        id_cardapio=int(request.form['id_cardapio'])
    )
    print(favorito)
    # Salvando o produto no banco
    db_session.add(favorito)
    favorito.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': favorito.id_favorito,
        'id_cliente': favorito.id_cliente,
        'id_cardapio': favorito.id_cardapio
    }
    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getFavorito/<id>', methods=['GET'])
def get_favorite(id):
    favorito = Favorito.query.all()
    result = []
    for consulta in favorito:
        result.append(consulta.serialize_favorito())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/deleteFavorito/<id>', methods=['DELETE'])
def delete_favorite(id):
    favorito = select(Favorito).where(Favorito.id_favorito == id)
    favorito = db_session.execute(favorito).scalar()
    final = {
        'status': 'removido',
        'id': favorito.id_favorito,
        'id_cliente': favorito.id_cliente,
        'id_cardapio': favorito.id_cardapio
    }
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addFavorito_cliente', methods=['POST'])
def add_favorite_cliente():
    favorito_cliente = Favorito_cliente(
        id_cliente=int(request.form['id_cliente']),
        id_favorito=int(request.form['id_favorito'])
    )
    print(favorito_cliente)
    # Salvando o produto no banco
    db_session.add(favorito_cliente)
    favorito_cliente.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': favorito_cliente.id_favorito_cliente,
        'id_cliente': favorito_cliente.id_cliente,
        'id_favorito': favorito_cliente.id_favorito
    }
    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getFavorito_cliente/<id>', methods=['GET'])
def get_favorite_client(id):
    favorito_cliente = Favorito_cliente.query.all()
    result = []
    for consulta in favorito_cliente:
        result.append(consulta.serialize_favorito_cliente())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/deleteFavorito_cliente/<id>', methods=['DELETE'])
def delete_favorite_client(id):
    favorito_cliente = select(Favorito_cliente).where(Favorito_cliente.id_favorito_cliente == id)
    favorito_cliente = db_session.execute(favorito_cliente).scalar()
    final = {
        'status': 'removido',
        'id': favorito_cliente.id_favorito_cliente,
        'id_cliente': favorito_cliente.id_cliente,
        'id_favorito': favorito_cliente.id_favorito
    }
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addFavorito_cardapio', methods=['POST'])
def add_favorite_cardapio():
    favorito_cardapio = Favorito_Cardapio(
        id_favorito=int(request.form['id_favorito']),
        id_cardapio=int(request.form['id_cardapio'])
    )
    print(favorito_cardapio)
    # Salvando o produto no banco
    db_session.add(favorito_cardapio)
    favorito_cardapio.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': favorito_cardapio.id_favorito_cardapio,
        'id_cardapio': favorito_cardapio.id_cardapio,
        'id_favorito': favorito_cardapio.id_favorito
    }
    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getFavorito_cardapio/<id>', methods=['GET'])
def get_favorite_cardapio(id):
    favorito_cardapio = Favorito_Cardapio.query.all()
    result = []
    for consulta in favorito_cardapio:
        result.append(consulta.serialize_favorito_cardapio())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/deleteFavorito_cardapio/<id>', methods=['DELETE'])
def delete_favorite_cardapio(id):
    favorito_cardapio = select(Favorito_Cardapio).where(Favorito_Cardapio.id_favorito_cardapio == id)
    favorito_cardapio = db_session.execute(favorito_cardapio).scalar()
    final = {
        'status': 'removido',
        'id': favorito_cardapio.id_favorito_cardapio,
        'id_cardapio': favorito_cardapio.id_cardapio,
        'id_favorito': favorito_cardapio.id_favorito
    }
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addNota', methods=['POST'])
def add_nota():
    nota = Notas(
        id_empresa=int(request.form['id_empresa']),
        id_cliente=int(request.form['id_cliente'])

    )
    print(nota)
    # Salvando o produto no banco
    db_session.add(nota)
    nota.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': nota.id_notas,
        'id_cliente': nota.id_cliente,
        'id_empresa': nota.id_empresa

    }
    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getNota/<id>', methods=['GET'])
def get_nota(id):
    nota = Notas.query.all()
    result = []
    for consulta in nota:
        result.append(consulta.serialize_nota())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/updateNota/<id>', methods=['PUT'])
def update_nota(id):
    nota = select(Notas).where(Notas.id_notas == id)
    nota = db_session.execute(nota).scalar()
    db_session.commit()
    final = {
        'status': 'atualizado',
        'id': nota.id_notas,
        'id_cliente': nota.id_cliente,
        'id_empresa': nota.id_empresa
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/deleteNota/<id>', methods=['DELETE'])
def delete_nota(id):
    nota = select(Notas).where(Notas.id_notas == id)
    nota = db_session.execute(nota).scalar()
    final = {
        'status': 'removido',
        'id': nota.id_notas,
        'id_cliente': nota.id_cliente,
        'id_empresa': nota.id_empresa
    }
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/addCliente_notas', methods=['POST'])
def add_cliente_notas():
    cliente_nota = Cliente_Nota(
        id_cliente=int(request.form['id_cliente']),
        id_notas=int(request.form['id_notas'])
    )
    print(cliente_nota)
    # Salvando o produto no banco
    db_session.add(cliente_nota)
    cliente_nota.save()

    # Resposta em JSON
    final = {
        'status': 'sucesso',
        'id': cliente_nota.id_cliente_nota,
        'id_cliente': cliente_nota.id_cliente,
        'id_notas': cliente_nota.id_notas
    }
    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


@app.route('/getCliente_notas/<id>', methods=['GET'])
def get_cliente_notas(id):
    cliente_nota = Cliente_Nota.query.all()
    result = []
    for consulta in cliente_nota:
        result.append(consulta.serialize_cliente_nota())
    final = json.dumps(result)
    print(final)
    return Response(response=final,
                    status=200,
                    mimetype='application/json')


@app.route('/updateCliente_notas/<id>', methods=['PUT'])
def update_cliente_notas(id):
    cliente_nota = select(Cliente_Nota).where(Cliente_Nota.id_cliente_nota == id)
    cliente_nota = db_session.execute(cliente_nota).scalar()
    db_session.commit()
    final = {
        'status': 'atualizado',
        'id': cliente_nota.id_cliente_nota,
        'id_cliente': cliente_nota.id_cliente,
        'id_notas': cliente_nota.id_notas
    }
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/deleteCliente_notas/<id>', methods=['DELETE'])
def delete_cliente_notas(id):
    cliente_nota = select(Cliente_Nota).where(Cliente_Nota.id_cliente_nota == id)
    cliente_nota = db_session.execute(cliente_nota).scalar()

    final = {
        'status': 'removido',
        'id': cliente_nota.id_cliente_nota,
        'id_cliente': cliente_nota.id_cliente,
        'id_notas': cliente_nota.id_notas
    }
    db_session.commit()
    return Response(response=json.dumps(final),
                    status=200,
                    mimetype='application/json')


@app.route('/login_empresa', methods=['POST'])
def login_empresa():
    cnpj=int(request.form['cnpj'])
    senha=str(request.form['senha'])
    conectado = False

    empresa_sql = select(Empresa).where(Empresa.cnpj_empresa == cnpj)
    empresa = db_session.execute(empresa_sql).scalar()

    if empresa is None:
        final = {
            'status': 'success',
            'msg_erro': 'Essa empresa não existe'
        }
    else:
        conectado = senha == empresa.senha_empresa
    # empresa = consultar_empresa_cnpj(cnpj).json
    # print(empresa)
    # Resposta em JSON
        final = {
            'status': 'sucesso',
            'cnpj': cnpj,
            'conectado': conectado
        }

    return app.response_class(
        response=json.dumps(final),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(debug=True)
