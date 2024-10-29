# importar bibliotecas
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

# configurar banco
engine = create_engine('sqlite:///food.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Cliente(Base):
    __tablename__ = 'clientes'
    id_cliente = Column(Integer, primary_key=True)
    nome_cliente = Column(String(40), nullable=True)
    senha_cliente = Column(String(40), nullable=True)
    telefone_cliente = Column(Integer, nullable=True)
    email_cliente = Column(String(40), nullable=True)
    endereco_cliente = Column(String(40), nullable=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_cliente(self):
        dados_clientes = {
            'id_cliente': self.id_cliente,
            'nome_cliente': self.nome_cliente,
            'senha_cliente': self.senha_cliente,
            'telefone_cliente': self.telefone_cliente,
            'email_cliente': self.email_cliente,
            'endereco_cliente': self.endereco_cliente
        }
        return dados_clientes

    def __repr__(self):
        return '<clientes: {} {} {} {} {} {}>'.format(self.id_cliente,
                                                      self.nome_cliente,
                                                      self.senha_cliente,
                                                      self.telefone_cliente,
                                                      self.email_cliente,
                                                      self.endereco_cliente)


class Cardapio(Base):
    __tablename__ = 'cardapios'
    id_cardapio = Column(Integer, primary_key=True)
    nome_cardapio = Column(String(40), nullable=True)
    descricao_cardapio = Column(String(40), nullable=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_cardapio(self):
        dados_cardapio = {
            'id_cardapio': self.id_cardapio,
            'nome_cardapio': self.nome_cardapio,
            'descricao_cardapio': self.descricao_cardapio
        }
        return dados_cardapio

    def __repr__(self):
        return '<cardapio: {} {} {}>'.format(self.id_cardapio,
                                             self.nome_cardapio,
                                             self.descricao_cardapio)


class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria = Column(Integer, primary_key=True, nullable=True)
    nome_Categoria = Column(String(40), nullable=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_categoria(self):
        dados_categoria = {
            'id_Categoria': self.id_categoria,
            'nome_Categoria': self.nome_Categoria
        }
        return dados_categoria

    def __repr__(self):
        return '<categorias: {} {}>'.format(self.id_categoria,
                                            self.nome_Categoria)


class Produto(Base):
    __tablename__ = 'produtos'
    id_produto = Column(Integer, primary_key=True, nullable=True)
    nome_produto = Column(String(40), nullable=True)
    preco_produto = Column(Float, nullable=True)
    disponivel = Column(Integer, nullable=True)
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))
    categorias = relationship(Categoria)
    id_cardapio = Column(Integer, ForeignKey('cardapios.id_cardapio'))
    cardapios = relationship(Cardapio)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_produto(self):
        dados_produtos = {
            'id_produto': self.id_produto,
            'nome_produto': self.nome_produto,
            'preco_produto': self.preco_produto,
            'disponivel': self.disponivel,
            'id_categoria': self.id_categoria,
            'id_cardapio': self.id_cardapio
        }
        return dados_produtos

    def __repr__(self):
        return '<produto>'.format(self.nome_produto)


class Carrinho(Base):
    __tablename__ = 'carrinhos'
    id_carrinho = Column(Integer, primary_key=True)
    data_pedido = Column(String(10), nullable=True)
    quantidade = Column(Integer, nullable=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    clientes = relationship(Cliente)
    id_produto = Column(Integer, ForeignKey('produtos.id_produto'))
    produtos = relationship(Produto)
    tempo_producao = Column(Integer, nullable=True)
    preco_total = Column(Float, nullable=True)
    status = Column(Integer, nullable=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_carrinho(self):
        dados_carrinho = {
            'id_carrinho': self.id_carrinho,
            'data_pedido': self.data_pedido,
            'quantidade': self.quantidade,
            'id_cliente': self.id_cliente,
            'id_produto': self.id_produto,
            'tempo_producao': self.tempo_producao,
            'preco_total': self.preco_total,
            'status': self.status
        }
        return dados_carrinho

    def __repr__(self):
        return '<carrinhos: {} {} {} {} {} {} {} {}>'.format(self.id_carrinho,
                                                             self.data_pedido,
                                                             self.quantidade,
                                                             self.id_cliente,
                                                             self.id_produto,
                                                             self.tempo_producao,
                                                             self.preco_total,
                                                             self.status)


class Empresa(Base):
    __tablename__ = 'empresas'
    id_empresa = Column(Integer, primary_key=True)
    nome_empresa = Column(String(40), nullable=True)
    endereco_empresa = Column(String(40), nullable=True)
    id_cardapio = Column(Integer, ForeignKey('cardapios.id_cardapio'), nullable=True)
    cnpj_empresa = Column(Integer, unique=True, nullable=False)
    senha_empresa = Column(String(40), nullable=True)
    email_empresa = Column(String(40), nullable=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_empresa(self):
        dados_empresa = {
            'id_empresa': self.id_empresa,
            'nome_empresa': self.nome_empresa,
            'endereco_empresa': self.endereco_empresa,
            'id_cardapio': self.id_cardapio,
            'cnpj_empresa': self.cnpj_empresa,
            'email_empresa': self.email_empresa,
            'senha_empresa': self.senha_empresa
        }
        return dados_empresa

    def __repr__(self):
        return '<Empresa:>'.format(self.id_empresa,
                                   self.nome_empresa,
                                   self.endereco_empresa,
                                   self.cnpj_empresa,
                                   self.email_empresa,
                                   self.senha_empresa)


class Ingrediente(Base):
    __tablename__ = 'ingredientes'
    id_ingrediente = Column(Integer, primary_key=True)
    nome_ingrediente = Column(String(40), nullable=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_ingrediente(self):
        dados_ingrediente = {
            'id_ingrediente': self.id_ingrediente,
            'nome_ingrediente': self.nome_ingrediente
        }
        return dados_ingrediente

    def __repr__(self):
        return '<ingredientes: {} {}>'.format(self.id_ingrediente,
                                              self.nome_ingrediente)


class Ingrediente_produto(Base):
    __tablename__ = 'ingredientes_produtos'
    id_ingrediente_produto = Column(Integer, primary_key=True)
    id_produto = Column(Integer, ForeignKey('produtos.id_produto'), nullable=True)
    produtos = relationship(Produto)
    id_ingrediente = Column(Integer, ForeignKey('ingredientes.id_ingrediente'), nullable=True)
    ingredientes = relationship(Ingrediente)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_ingrediente_produto(self):
        dados_ingredientePro = {
            'id_produto': self.id_produto,
            'id_ingrediente': self.id_ingrediente
        }
        return dados_ingredientePro

    def __repr__(self):
        return '<ingredientes_produtos: {} {} >'.format(self.id_produto,
                                                        self.id_ingrediente)


class Favorito(Base):
    __tablename__ = 'favoritos'
    id_favorito = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    clientes = relationship(Cliente)
    id_cardapio = Column(Integer, ForeignKey('cardapios.id_cardapio'))
    cardapios = relationship(Cardapio)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_favorito(self):
        dados_favorito = {
            'id_favorito': self.id_favorito,
            'id_cliente': self.id_cliente,
            'id_cardapio': self.id_cardapio
        }
        return dados_favorito

    def __repr__(self):
        return '<favoritos: {} {} {}>'.format(self.id_favorito,
                                              self.id_cliente,
                                              self.id_cardapio)


class Favorito_cliente(Base):
    __tablename__ = 'favoritos_clientes'
    id_favorito_cliente = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=True)
    clientes = relationship(Cliente)
    id_favorito = Column(Integer, ForeignKey('favoritos.id_favorito'), nullable=True)
    favoritos = relationship(Favorito)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_favorito_cliente(self):
        dados_favoritoC = {
            'id_cliente': self.id_cliente,
            'id_favorito': self.id_favorito
        }
        return dados_favoritoC

    def __repr__(self):
        return '<favoritos_clientes: {} {}>'.format(self.id_cliente,
                                                    self.id_favorito)


class Favorito_Cardapio(Base):
    __tablename__ = 'favoritos_cardapios'
    id_favorito_cardapio = Column(Integer, primary_key=True)
    id_cardapio = Column(Integer, ForeignKey('cardapios.id_cardapio'), nullable=True)
    cardapios = relationship(Cardapio)
    id_favorito = Column(Integer, ForeignKey('favoritos.id_favorito'), nullable=True)
    favoritos = relationship(Favorito)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_favorito_cardapio(self):
        dados_favoritoCar = {
            'id_cardapio': self.id_cardapio,
            'id_favorito': self.id_favorito
        }
        return dados_favoritoCar

    def __repr__(self):
        return '<favoritos_cardapios: {} {}>'.format(self.id_cardapio,
                                                     self.id_favorito)


class Notas(Base):
    __tablename__ = 'notas'
    id_notas = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=True)
    cliente = relationship(Cliente)
    id_empresa = Column(Integer, ForeignKey('empresas.id_empresa'), nullable=True)
    empresa = relationship(Empresa)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_nota(self):
        dados_nota = {
            'id_empresa': self.id_empresa,
            'id_cliente': self.id_cliente
        }
        return dados_nota

    def __repr__(self):
        return '<Cliente_Nota: {} {}>'.format(self.id_notas,
                                              self.id_cliente)


class Cliente_Nota(Base):
    __tablename__ = 'clientes_notas'
    id_cliente_nota = Column(Integer, primary_key=True)
    id_notas = Column(Integer, nullable=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=True)
    clientes = relationship(Cliente)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_cliente_nota(self):
        dados_notasCli = {
            'id_notas': self.id_notas,
            'id_cliente': self.id_cliente
        }
        return dados_notasCli

    def __repr__(self):
        return '<Cliente_Nota: {} {}>'.format(self.id_notas,
                                              self.id_cliente)

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
