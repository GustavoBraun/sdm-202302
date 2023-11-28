from flask import Flask
from flask_restx import reqparse, abort, Api, Resource, fields

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='Atividade 15',
          description='Atividade REST 15')

PRODUTOS = [{'id' : 0, 'nome': 'sapato', 'quantidade' : 52, 'preco': 123.55},
            {'id' : 1, 'nome': 'camisa','quantidade' : 26, 'preco': 50.55},
            {'id' : 2, 'nome': 'calça', 'quantidade' : 142,'preco': 112.55},
            {'id' : 3, 'nome': 'bermuda', 'quantidade' : 15, 'preco': 73.55}]

TRABALHADORES = [{'cpf': 0, 'nome': 'Ana', 'horasTrabalhadas': 8, 'valorHora' : 45.78},
{'cpf': 1, 'nome': 'Bruna', 'horasTrabalhadas': 2, 'valorHora' : 60.00},
{'cpf': 2, 'nome': 'Carlos', 'horasTrabalhadas': 10, 'valorHora' : 38.99},
{'cpf': 3, 'nome': 'Diogo', 'horasTrabalhadas': 4, 'valorHora' : 45.78},
{'cpf': 4, 'nome': 'Ester', 'horasTrabalhadas': 5, 'valorHora' : 45.78}]

def aborta_se_o_produto_nao_existe(id):
    encontrei = False
    for produto in PRODUTOS:
        if produto['id'] == int(id):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem="O produto com id {} não foi encontrado".format(id))
    
    
def aborta_se_o_trabalhador_nao_existe(cpf):
    encontrei = False
    for trabalhador in TRABALHADORES:
        if trabalhador['cpf'] == int(cpf):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem="Trabalhador com cpf = {} não existe".format(cpf)) #404:Not Found
        
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='Identificador do produto.')
parser.add_argument('nome', type=str, help='Nome do produto.')
parser.add_argument('quantidade', type=int, help='Quantidade de produtos em estoque.')
parser.add_argument('preco', type=float, help='Preço do produto.')

parserTrabalhador = reqparse.RequestParser()
parserTrabalhador.add_argument('cpf', type=int, help='CPF do trabalhador')
parserTrabalhador.add_argument('nome', type=str, help='nome do trabalhador')
parserTrabalhador.add_argument('horasTrabalhadas', type=int, help='Quantidade de horas trabalhadas')
parserTrabalhador.add_argument('valorHora', type=float, help='Valor da hora')

campos_obrigatorios_para_atualizacao_produto = api.model('Atualização de Produto', {
    'id' : fields.Integer(required = True, description='Identificador do produto.'),
    'nome' : fields.String(required = True, description = "Nome do produto."),
    'quantidade' : fields.Integer(required = True, description = "Quantidade de produtos em estoque."),
    'preco' : fields.Float(required = True, description = "Valor do produto."),
})


campos_obrigatorios_para_atualizacao_produto_id = api.model('Atualização de Produto', {
    'id' : fields.Integer(required = True, description='Identificador do produto.'),
    'nome' : fields.String(required = False, description = "Nome do produto."),
    'quantidade' : fields.Integer(required = False, description = "Quantidade de produtos em estoque."),
    'preco' : fields.Float(required = False, description = "Valor do produto."),
})

campos_obrigatorios_para_atualizacao_produto_nome = api.model('Atualização de Produto', {
    'id' : fields.Integer(required = False, description='Identificador do produto.'),
    'nome' : fields.String(required = True, description = "Nome do produto."),
    'quantidade' : fields.Integer(required = False, description = "Quantidade de produtos em estoque."),
    'preco' : fields.Float(required = False, description = "Valor do produto."),
})

campos_obrigatorios_para_atualizacao_produto_quantidade = api.model('Atualização de Produto', {
    'id' : fields.Integer(required = False, description='Identificador do produto.'),
    'nome' : fields.String(required = False, description = "Nome do produto."),
    'quantidade' : fields.Integer(required = True, description = "Quantidade de produtos em estoque."),
    'preco' : fields.Float(required = False, description = "Valor do produto."),
})


campos_obrigatorios_para_atualizacao_preco = api.model('Atualização de Produto', {
    'id' : fields.Integer(required = False, description='Identificador do produto.'),
    'nome' : fields.String(required = False, description = "Nome do produto."),
    'quantidade' : fields.Integer(required = False, description = "Quantidade de produtos em estoque."),
    'preco' : fields.Float(required = True, description = "Valor do produto."),
})

campos_obrigatorios_para_insercao_produto = api.model('Inserção de Produto', {
    'id' : fields.Integer(required = False, readonly = True, description='Identificador do produto.'),
    'nome' : fields.String(required = True, description = "Nome do produto."),
    'quantidade' : fields.Integer(required = True, description = "Quantidade de produtos em estoque."),
    'preco' : fields.Float(required = True, description = "Valor do produto."),
})

campos_obrigatorios_para_atualizacao_trabalhador = api.model('Atualização de trabalhador', {
    'cpf' : fields.Integer(required = True, description = 'CPF do trabalhador.'),
    'nome' : fields.String(required = True, description = "Nome do trabalhador."),
    'horasTrabalhadas' : fields.Integer(required = True, description = "Quantidade de horas que o trabalhador trabalha durante a semana."),
    'valorHora' : fields.Float(required = True, description = "Quantidade que o trabalhador recebe por hora."),
})
campos_obrigatorios_para_atualizacao_nome_trabalhador = api.model('Atualização de trabalhador', {
    'cpf' : fields.Integer(required = False, description = 'CPF do trabalhador.'),
    'nome' : fields.String(required = True, description = "Nome do trabalhador."),
    'horasTrabalhadas' : fields.Integer(required = False, description = "Quantidade de horas que o trabalhador trabalha durante a semana."),
    'valorHora' : fields.Float(required = False, description = "Quantidade que o trabalhador recebe por hora."),
})

campos_obrigatorios_para_insercao_trabalhador = api.model('Inserção trabalhador', {
    'cpf' : fields.Integer(required = False, readonly = True, description = 'CPF do trabalhador.'),
    'nome' : fields.String(required = True, description = "Nome do trabalhador."),
    'horasTrabalhadas' : fields.Integer(required = True, description = "Quantidade de horas que o trabalhador trabalha durante a semana."),
    'valorHora' : fields.Float(required = True, description = "Quantidade que o trabalhador recebe por hora."),
})


@api.route('/trabalhadores/<cpf>')
@api.doc(params={'cpf' : 'CPF do trabalhador'})
class Trabalhador(Resource):
    @api.doc(responses={200 : "Trabalhador retornado"})
    def get(self, cpf):
        aborta_se_o_trabalhador_nao_existe(cpf)
        return TRABALHADORES[int(cpf)]

    @api.doc(responses={204 : 'Trabalhador removido'})
    def delete(self, cpf): 
        aborta_se_o_trabalhador_nao_existe(cpf)
        del TRABALHADORES[int(cpf)]
        return '', 204
    
    
    @api.doc(responses={200 : 'Trabalhador substituído'})
    @api.expect(campos_obrigatorios_para_atualizacao_trabalhador)
    def put(self, cpf):
        aborta_se_o_trabalhador_nao_existe(cpf)
        args = parserTrabalhador.parse_args()
        for trabalhador in TRABALHADORES:
            if trabalhador['cpf'] == int(cpf):
                trabalhador['cpf'] = args['cpf']
                trabalhador['nome'] = args['nome']
                trabalhador['horasTrabalhadas'] = args['horasTrabalhadas']
                trabalhador['valorHora'] = args['valorHora'] 
                break
        return trabalhador

@api.route('/trabalhadores/pagamentos')
class ListaPagamentos(Resource):
    def get(self):
        PAGAMENTOS = []
        for trabalhador in TRABALHADORES:
            pagamento = {"Trabalhador" : trabalhador['nome'], "Pagamento" : trabalhador['horasTrabalhadas'] * trabalhador['valorHora']}    
            PAGAMENTOS.append(pagamento)
        return PAGAMENTOS

@api.route('/trabalhadores/pagamentos/<cpf>')
@api.doc(params = {'cpf' : 'CPF do trabalhador.'})
class Pagamentos(Resource):
    def get(self, cpf):
        for trabalhador in TRABALHADORES:
            if int(cpf) == trabalhador['cpf']:
                pagamento = trabalhador['horasTrabalhadas'] * trabalhador['valorHora']
                break
        return pagamento
    
@api.route('/trabalhadores')
class ListaTrabalhador(Resource):
    @api.doc(response={200: 'Trabalhadores retornados'})
    def get(self):
        return TRABALHADORES
    
    @api.doc(response={201 : 'Trabalhador criado.'})
    @api.expect(campos_obrigatorios_para_insercao_trabalhador)
    def post(self):
        args = parserTrabalhador.parse_args()
        cpf = -1
        for trabalhador in TRABALHADORES:
            if int(trabalhador['cpf']) > cpf:
                cpf = int(trabalhador['cpf'])
        cpf += 1
        trabalhador = {'cpf' : cpf, 'nome' : args['nome'], 'horasTrabalhadas' : args['horasTrabalhadas'], 'valorHora' : args['valorHora']}
        TRABALHADORES.append(trabalhador)
        return trabalhador, 201
    
@api.route('/trabalhadores/menorSalario')        
class MenorSalario(Resource):
    @api.doc(response={200: 'Menor salário retornado'})
    def get(self):
        menorSalario = 100000
        for trabalhador in TRABALHADORES:
            salario = trabalhador['horasTrabalhadas'] * trabalhador['valorHora']
            if menorSalario > salario:
                menorSalario = salario
        return menorSalario

@api.route('/trabalhadores/maiorSalario')
class MaiorSalario(Resource):
    @api.doc(response={200: 'Maior salário retornado'})
    def get(self):
        maiorSalario = -1
        for trabalhador in TRABALHADORES:
            salario = trabalhador['horasTrabalhadas'] * trabalhador['valorHora']
            if maiorSalario < salario:
                maiorSalario = salario
        return maiorSalario

@api.route('/trabalhadores/totalPagar')
class TotalASePagar(Resource):
    @api.doc(response={200: 'Total a se pagar'})
    def get(self):
        salario = 0
        for trabalhador in TRABALHADORES:
            salario += trabalhador['horasTrabalhadas'] * trabalhador['valorHora']
        return salario

@api.route('/trabalhadores/AtualizaNome/<cpf>')
class AtualizarPorNome(Resource):
    @api.doc(response={200: "Trabalhador atualizado"})
    @api.expect(campos_obrigatorios_para_atualizacao_nome_trabalhador)
    def put(self, cpf):
        aborta_se_o_trabalhador_nao_existe(cpf)
        args = parserTrabalhador.parse_args()
        for trabalhador in TRABALHADORES:
            if trabalhador['cpf'] == int(cpf):
                trabalhador['nome'] = args['nome']
                break
        return trabalhador
    
@api.route('/trabalhadores/AtualizaCpf/<cpf>')
class AtualizarPorNome(Resource):
    @api.doc(response={200: "Trabalhador atualizado"})
    @api.expect(campos_obrigatorios_para_atualizacao_nome_trabalhador)
    def put(self, cpf):
        aborta_se_o_trabalhador_nao_existe(cpf)
        args = parserTrabalhador.parse_args()
        for trabalhador in TRABALHADORES:
            if trabalhador['cpf'] == int(cpf):
                trabalhador['cpf'] = args['cpf']
                break
        return trabalhador
    
@api.route('/trabalhadores/AtualizaHorasTrabalhadas/<cpf>')
class AtualizarPorNome(Resource):
    @api.doc(response={200: "Trabalhador atualizado"})
    @api.expect(campos_obrigatorios_para_atualizacao_nome_trabalhador)
    def put(self, cpf):
        aborta_se_o_trabalhador_nao_existe(cpf)
        args = parserTrabalhador.parse_args()
        for trabalhador in TRABALHADORES:
            if trabalhador['cpf'] == int(cpf):
                trabalhador['horasTrabalhadas'] = args['horasTrabalhadas']
                break
        return trabalhador

@api.route('/trabalhadores/AtualizaValorHora/<cpf>')
class AtualizarPorNome(Resource):
    @api.doc(response={200: "Trabalhador atualizado"})
    @api.expect(campos_obrigatorios_para_atualizacao_nome_trabalhador)
    def put(self, cpf):
        aborta_se_o_trabalhador_nao_existe(cpf)
        args = parserTrabalhador.parse_args()
        for trabalhador in TRABALHADORES:
            if trabalhador['cpf'] == int(cpf):
                trabalhador['valorHora'] = args['valorHora']
                break
        return trabalhador

@api.route('/produtos/<id>')
@api.doc(params={'id' : 'identificador do produto'})
class Produto(Resource):
    @api.doc(responses={200 : 'Produto retornado'})
    def get(self, id):
        aborta_se_o_produto_nao_existe(id)
        return PRODUTOS[int(id)]

    @api.doc(responses={204: 'Produto removido'})
    def delete(self, id):
        aborta_se_o_produto_nao_existe(id)
        del PRODUTOS[int(id)]
        return '', 204
    
    @api.doc(responses={200: 'Produto substituído.'})
    @api.expect(campos_obrigatorios_para_atualizacao_produto)
    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['id'] = args['id']
                produto['nome'] = args['nome']
                produto['quantidade'] = args['quantidade']
                produto['preco'] = args['preco']
                PRODUTOS[int(id)]
                break    
        return produto, 200

@api.route('/produtos/atualizaID/<id>')
@api.doc(params={'id' : 'Identificador do produto.'})
class AtualizaID(Resource):
    @api.doc(responses={200: 'Produto atualizado'})
    @api.expect(campos_obrigatorios_para_atualizacao_produto_id)
    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['id'] = args['id']
                break
        return produto
    
@api.route('/produtos/atualizaNome/<id>')
@api.doc(params={'id' : 'Identificador do produto.'})
class AtualizaID(Resource):
    @api.doc(responses={200: 'Produto atualizado'})
    @api.expect(campos_obrigatorios_para_atualizacao_produto_id)
    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['nome'] = args['nome']
                break
        return produto
    
@api.route('/produtos/atualizaQuantidade/<id>')
@api.doc(params={'id' : 'Identificador do produto.'})
class AtualizaID(Resource):
    @api.doc(responses={200: 'Produto atualizado'})
    @api.expect(campos_obrigatorios_para_atualizacao_produto_id)
    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['quantidade'] = args['quantidade']
                break
        return produto

@api.route('/produtos/atualizaPreco/<id>')
@api.doc(params={'id' : 'Identificador do produto.'})
class AtualizaID(Resource):
    @api.doc(responses={200: 'Produto atualizado'})
    @api.expect(campos_obrigatorios_para_atualizacao_produto_id)
    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['preco'] = args['preco']
                break
        return produto
    
@api.route('/produtos/estoque')
class ListaEstoque(Resource):
    @api.doc(responses={200: 'Estoque retornado.'})
    def get(self):
        ESTOQUES = []
        for produto in PRODUTOS:
            estoque = {'Nome' : produto['nome'], 'Quantidade' : produto['quantidade']}
            ESTOQUES.append(estoque)
        return ESTOQUES
    
@api.route('/produtos/estoque/<id>')
@api.doc(params={'id' : 'Identificador do produto.'})
class Estoque(Resource):
    @api.doc(responses={200: 'Estoque do produto retornado.'})
    def get(self, id):
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                estoque = {'Nome' : produto['nome'], 'Quantidade' : produto['quantidade']}
                break
        return estoque

@api.route('/produtos/estoque/venda/<id>')
@api.doc(params={'id' : 'Identificador do produto.'})
class Estoque(Resource):
    @api.doc(responses={200: 'Venda efetuada.'})
    def put(self, id):
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['quantidade'] -= 1
                break
        return produto

@api.route('/produtos/estoque/compra/<id>')
@api.doc(params={'id' : 'Identificador do produto.'})
class Estoque(Resource):
    @api.doc(responses={200: 'Compra efetuada.'})
    def put(self, id):
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['quantidade'] += 1
                break
        return produto


@api.route('/produtos/estoque/menorQuantidade')
class MenorEstoque(Resource):
    @api.doc(responses={200: 'Menor estoque retornado.'})
    def get(self):
        menorEstoque = {'id' : -1, 'nome': '', 'quantidade' : 10000, 'preco': 0} 
        for produto in PRODUTOS:
            if produto['quantidade'] < menorEstoque['quantidade']:
                menorEstoque = {'id' : produto['id'], 'nome': produto['nome'], 'quantidade' : produto['quantidade'], 'preco': produto['preco']}
        return menorEstoque

@api.route('/produtos/estoque/maiorQuantidade')
class MaiorEstoque(Resource):
    @api.doc(responses={200: 'Menor estoque retornado.'})
    def get(self):
        maiorEstoque = {'id' : -1, 'nome': '', 'quantidade' : -1, 'preco': 0} 
        for produto in PRODUTOS:
            if produto['quantidade'] > maiorEstoque['quantidade']:
                maiorEstoque = {'id' : produto['id'], 'nome': produto['nome'], 'quantidade' : produto['quantidade'], 'preco': produto['preco']}
        return maiorEstoque


@api.route('/produtos/estoque/valorTotal')
class ValorTotal(Resource):
    @api.doc(responses={200: 'Valor total do estoque retornado.'})
    def get(self):
        valorTotal = 0
        for produto in PRODUTOS:
            valorTotal += produto['quantidade'] * produto['preco']
        return valorTotal

@api.route('/produtos')
class ListaProduto(Resource):
    @api.doc(responses={200: 'produtos retornados'})
    def get(self):
        return PRODUTOS
    
    @api.doc(responses={201: 'Produto inserido.'})
    @api.expect(campos_obrigatorios_para_insercao_produto)
    def post(self):
        args = parser.parse_args()
        id = -1
        for produto in PRODUTOS:
            if int(produto['id']) > id:
                id = int(produto['id'])
        id += 1
        produto = {'id' : id, 'nome' : args['nome'], 'quantidade' : args['quantidade'], 'preco' : args['preco']}
        PRODUTOS.append(produto)
        return produto, 201

if __name__ == '__main__':
    app.run(debug=True)