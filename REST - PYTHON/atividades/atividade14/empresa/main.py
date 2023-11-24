from flask import Flask
from flask_restx import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TRABALHADORES = [{'cpf': 1, 'nome': 'Ana', 'horasTrabalhadas': 8, 'valorHora' : 45.78},
{'cpf': 2, 'nome': 'Bruna', 'horasTrabalhadas': 2, 'valorHora' : 60.00},
{'cpf': 3, 'nome': 'Carlos', 'horasTrabalhadas': 10, 'valorHora' : 38.99},
{'cpf': 4, 'nome': 'Diogo', 'horasTrabalhadas': 4, 'valorHora' : 45.78},
{'cpf': 5, 'nome': 'Ester', 'horasTrabalhadas': 5, 'valorHora' : 45.78}]

def aborta_se_o_trabalhador_nao_existe(cpf):
    encontrei = False
    for trabalhador in TRABALHADORES:
        if trabalhador['cpf'] == int(cpf):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem="Trabalhador com cpf = {} não existe".format(cpf)) #404:Not Found
# Parse dos dados enviados na requisição no formato JSON:
parser = reqparse.RequestParser()
parser.add_argument('cpf', type=int, help='CPF do trabalhador')
parser.add_argument('nome', type=str, help='nome do trabalhador')
parser.add_argument('horasTrabalhadas', type=int, help='Quantidade de horas trabalhadas')
parser.add_argument('valorHora', type=float, help='Valor da hora')
# Produto:
# 1) Apresenta um único produto.
# 2) Remove um único produto.
# 3) Atualiza (substitui) um produto.
class Trabalhador(Resource):
    def get(self, cpf):
        aborta_se_o_trabalhador_nao_existe(cpf)
        for trabalhador in TRABALHADORES:
            if trabalhador['cpf'] == int(cpf):
                return trabalhador
        
    def delete(self, cpf):
        aborta_se_o_trabalhador_nao_existe(cpf)
        del TRABALHADORES[int(cpf)]
        return '', 204, #204: No Content
    
    def put(self, cpf):
        aborta_se_o_trabalhador_nao_existe(cpf)
        args = parser.parse_args()
        for trabalhador in TRABALHADORES:
            if trabalhador['cpf'] == int(cpf):
                trabalhador['cpf'] = args['cpf']
                trabalhador['nome'] = args['nome']
                trabalhador['horasTrabalhadas'] = args['horasTrabalhadas']
                trabalhador['valorHora'] = args['valorHora']
                break
        return trabalhador, 200, #200: OK

class ListaPagamento(Resource):
    
    def get(self):
        SALARIOS = []
        for trabalhador in TRABALHADORES:
            salario = trabalhador['horasTrabalhadas'] * trabalhador['valorHora']
            SALARIOS.append({'cpf': trabalhador['cpf'], 'nome': trabalhador['nome'], 'salario' : salario})
        return SALARIOS
    
class MenorSalario(Resource):
    def get(self):
        menorSalario = 100000
        for trabalhador in TRABALHADORES:
            salario = trabalhador['horasTrabalhadas'] * trabalhador['valorHora']
            if menorSalario > salario:
                menorSalario = salario
        return menorSalario

class MaiorSalario(Resource):
    def get(self):
        maiorSalario = -1
        for trabalhador in TRABALHADORES:
            salario = trabalhador['horasTrabalhadas'] * trabalhador['valorHora']
            if maiorSalario < salario:
                maiorSalario = salario
        return maiorSalario

class TotalASePagar(Resource):
    def get(self):
        salario = 0
        for trabalhador in TRABALHADORES:
            salario += trabalhador['horasTrabalhadas'] * trabalhador['valorHora']
        return salario


# ListaProduto:
# 1) Apresenta a lista de produtos.
# 2) Insere um novo produto.
class ListaTrabalhador(Resource):
    def get(self):
        return TRABALHADORES

    def post(self):
        args = parser.parse_args()
        cpf = -1
        for trabalhador in TRABALHADORES:
            if int(trabalhador['cpf']) > cpf:
                cpf = int(trabalhador['cpf'])
        cpf = cpf + 1
        trabalhador = {'cpf': cpf, 'nome': args['nome'], 'horasTrabalhadas': args['horasTrabalhadas'], 'valorHora' : args['valorHora']}
        TRABALHADORES.append(trabalhador)
        return trabalhador, 201, #201: Created
    
##
## Roteamento de recursos:
##
api.add_resource(Trabalhador, '/trabalhadores/<cpf>')
api.add_resource(ListaTrabalhador, '/trabalhadores')
api.add_resource(ListaPagamento, '/trabalhadores/pagamento')
api.add_resource(MenorSalario, '/trabalhadores/menorSalario')
api.add_resource(MaiorSalario, '/trabalhadores/maiorSalario')
api.add_resource(TotalASePagar, '/trabalhadores/totalASePagar')

if __name__ == '__main__':
    app.run(debug=True)