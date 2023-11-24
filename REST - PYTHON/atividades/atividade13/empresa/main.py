from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

PRODUTOS = [{'id' : 0, 'nome': 'sapato', 'preco': 123.55},
            {'id' : 1, 'nome': 'camisa', 'preco': 50.55},
            {'id' : 2, 'nome': 'calça', 'preco': 112.55},
            {'id' : 3, 'nome': 'bermuda', 'preco': 73.55},]

ALUNOS = [{'matricula' : 0, 'nome' : 'Ana', 'nota' : 72.00},
          {'matricula' : 1, 'nome' : 'Bruna', 'nota' : 71.50},
          {'matricula' : 2, 'nome' : 'Carlos', 'nota' : 68.50},
          {'matricula' : 3, 'nome' : 'Diogo', 'nota' : 70.00},
          {'matricula' : 4, 'nome' : 'Ester', 'nota' : 69.00}]

def aborta_se_a_matricula_nao_existe(matricula):
    encontrei = False
    for aluno in ALUNOS:
        if aluno['matricula'] == int(matricula):
            encontrei = True
    if encontrei == False:
        abort(404, mensagme = "O aluno com matrícula {} não foi encontrado".format(matricula))

def aborta_se_o_produto_nao_existe(id):
    encontrei = False
    for produto in PRODUTOS:
        if produto['id'] == int(id):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem = "O produto com id = {} não existe".format(id))

parser = reqparse.RequestParser()
parserAlunos = reqparse.RequestParser()
parser.add_argument('id', type = int, help = 'ID identificador do protudo.')
parser.add_argument('nome', type = str, help = 'Nome do protudo.')
parser.add_argument('preco', type = float, help = 'Preço identificador do protudo.')

parserAlunos.add_argument('matricula', type = int, help = 'Matricula identificadora do aluno.')
parserAlunos.add_argument('nome', type = str, help = 'Nome do aluno.')
parserAlunos.add_argument('nota', type = float, help = 'Nota do aluno.')

class Aluno(Resource):
    def get(self, matricula):
        aborta_se_a_matricula_nao_existe(matricula)
        for aluno in ALUNOS:
            if aluno['matricula'] == int(matricula):
                return aluno
            
    def delete(self, matricula):
        aborta_se_a_matricula_nao_existe(matricula)
        del ALUNOS[int(matricula)]
        return '',204
    
    def put(self, matricula):
        aborta_se_a_matricula_nao_existe(matricula)
        args = parserAlunos.parse_args()
        for aluno in ALUNOS:
            if aluno['matricula'] == int(matricula):
                aluno['matricula'] = args['matricula']
                aluno['nome'] = args['nome']
                aluno['nota'] = args['nota']
                break
        return aluno, 200

class ListaAluno(Resource):
    def get(self):
        return ALUNOS
    
    def post(self):
        args = parserAlunos.parse_args()
        matricula = -1
        for aluno in ALUNOS:
            if int(aluno['matricula']) > matricula:
                matricula = int(aluno['matricula'])
        matricula += 1
        aluno = {'matricula': matricula, 'nome' : args['nome'], 'nota' : args['nota']}
        ALUNOS.append(aluno)
        return aluno, 200

class AtualizaNomeAluno(Resource):
    def put(self, matricula):
        aborta_se_a_matricula_nao_existe(matricula)
        args = parserAlunos.parse_args()
        for aluno in ALUNOS:
            if aluno['matricula'] == int(matricula):
                aluno['nome'] = args['nome']
                break
        return aluno, 200
    
class AtualizaMatriculaAluno(Resource):
    def put(self, matricula):
        aborta_se_a_matricula_nao_existe(matricula)
        args = parserAlunos.parse_args()
        for aluno in ALUNOS:
            if aluno['matricula'] == int(matricula):
                aluno['matricula'] = args['matricula']
                break
        return aluno, 200
    
class AtualizaNotaAluno(Resource):
    def put(self, matricula):
        aborta_se_a_matricula_nao_existe(matricula)
        args = parserAlunos.parse_args()
        for aluno in ALUNOS:
            if aluno['matricula'] == int(matricula):
                aluno['nota'] = args['nota']
                break
        return aluno, 200

class Produto(Resource):
    def get(self, id):
        aborta_se_o_produto_nao_existe(id)
        return PRODUTOS[int(id)]
            
    def delete(self, id):
        aborta_se_o_produto_nao_existe(id)
        del PRODUTOS[int(id)]
        return '', 204,

    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['id'] = args['id']
                produto['nome'] = args['nome']
                produto['preco'] = args['preco']
                break
        return produto, 200
    
class ProdutoSTR(Resource):
    def get(self, nome):
        for produto in PRODUTOS:
            if produto['nome'] == nome:
                return produto
        abort(404, mensagem = "O produto com nome = {} não existe".format(nome))

class ListaProduto(Resource):
    def get(self):
        return PRODUTOS
    
    def post(self):
        args = parser.parse_args()
        id = -1
        for produto in PRODUTOS:
            if int(produto['id']) > id :
                id = int(produto['id'])
        id = id + 1
        produto = {'id' : id, 'nome': args['nome'], 'preco' : args['preco']}
        PRODUTOS.append(produto)
        return produto, 201
    



api.add_resource(Produto, '/produtos/<id>')
api.add_resource(ListaProduto, '/produtos')
api.add_resource(ProdutoSTR, '/produtos-str/<nome>')
api.add_resource(Aluno, '/alunos/<matricula>')
api.add_resource(ListaAluno, '/alunos')
api.add_resource(AtualizaMatriculaAluno, '/aluno-matricula/<matricula>')
api.add_resource(AtualizaNomeAluno, '/aluno-nome/<matricula>')
api.add_resource(AtualizaNotaAluno, '/aluno-nota/<matricula>')

if __name__ == '__main__':
    app.run(debug = True)   